import secrets, hashlib, hmac, json
from models import Game
import uuid
from utils import logger

# simple deterministic bombs generation from server_seed
def generate_bombs(server_seed: str, w:int, h:int, bombs:int):
    cells = list(range(w*h))
    # expand server_seed to int
    seed_int = int(hashlib.sha256(server_seed.encode()).hexdigest(), 16)
    rng = secrets.SystemRandom(seed_int)
    rng.shuffle(cells)
    return sorted(cells[:bombs])

def new_game_engine(db, user_id, bet_amount, w=5, h=3, bombs=3):
    server_seed = secrets.token_hex(32)
    client_seed = secrets.token_hex(16)
    commit_hash = hashlib.sha256(server_seed.encode()).hexdigest()
    bomb_positions = generate_bombs(server_seed, w, h, bombs)
    gid = secrets.token_urlsafe(8)
    game = Game(
        id=gid,
        user_id=user_id,
        bet_amount=bet_amount,
        w=w,h=h,bombs=bombs,
        bomb_positions=bomb_positions,
        opened=[],
        state="playing",
        server_seed=server_seed,
        client_seed=client_seed,
        commit_hash=commit_hash
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    logger.info(f"New game {gid} for user {user_id} bombs={bomb_positions}")
    return gid, commit_hash, game

def reveal_cell(db, game: Game, idx: int):
    # if already opened - no-op
    if idx in (game.opened or []):
        return {"already": True, "lost": False}
    if game.state != "playing":
        return {"error": "not playing"}
    # open
    opened = game.opened or []
    opened.append(idx)
    # check bomb
    if idx in (game.bomb_positions or []):
        game.state = "lost"
        game.opened = opened
        db.add(game); db.commit(); db.refresh(game)
        logger.info(f"Game {game.id} LOST at idx {idx}")
        return {"lost": True}
    # safe
    game.opened = opened
    db.add(game); db.commit(); db.refresh(game)
    return {"lost": False, "opened": opened}

def compute_cashout(db, game: Game):
    # Sample payout calculation:
    safe_opened = len(game.opened or [])
    total_cells = game.w * game.h
    bombs = game.bombs
    safe_total = total_cells - bombs
    # simple linear multiplier: 1 + 0.1 * safe_opened (you should replace with real table)
    mult = 1 + 0.1 * safe_opened
    payout = float(game.bet_amount) * mult
    game.state = "cashed_out"
    db.add(game); db.commit(); db.refresh(game)
    logger.info(f"Game {game.id} cashed out {payout}")
    return payout

def render_grid_markup(game: Game, reveal_all: bool=False):
    # Build inline keyboard markup (simple string format for callback_data)
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width= game.w if game.w else 5)
    buttons = []
    total = game.w * game.h
    for idx in range(total):
        label = "⬜"
        if reveal_all or idx in (game.opened or []):
            if idx in (game.bomb_positions or []):
                label = "💣"
            else:
                label = "🔸"
        cb = f"m:{game.id}:c:{idx}"
        buttons.append(InlineKeyboardButton(label, callback_data=cb))
    # add cashout button
    buttons.append(InlineKeyboardButton("💰 Sacar", callback_data=f"m:{game.id}:cashout"))
    kb.add(*buttons)
    return kb
