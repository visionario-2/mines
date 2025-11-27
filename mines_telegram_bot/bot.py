import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from db import SessionLocal, engine, init_db
from models import User, Game
from mines_engine import new_game_engine, reveal_cell, render_grid_markup, compute_cashout
from utils import logger, ensure_user, rate_limit_check

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not set in env")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Initialize DB (creates tables)
init_db()

async def start_bot():
    # Use polling for simplicity on Render; you may switch to webhook mode if preferred.
    from aiogram import F
    from aiogram import exceptions
    await dp.start_polling(bot)

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    user = msg.from_user
    with SessionLocal() as db:
        ensure_user(db, user)
    await msg.answer("Bem-vindo! Use /play para iniciar um Mines.")

@dp.message(Command("play"))
async def cmd_play(msg: types.Message):
    # Rate-limit check
    user = msg.from_user
    if not rate_limit_check(user.id):
        await msg.answer("Você está fazendo ações rápido demais. Aguarde.")
        return

    # For demo: fixed bet. In production, integrate balance checks / deposits.
    bet = 100
    with SessionLocal() as db:
        user_model = ensure_user(db, user)
        # check balance omitted here - integrate with your payments system
        gid, commit_hash, game = new_game_engine(db, user_model.id, bet, w=5, h=3, bombs=3)
    text = f"🎮 Mines 5x3 - Aposta: {bet} satoshis\nCommit: <code>{commit_hash}</code>\nClique nas casas:"
    markup = render_grid_markup(game)
    await msg.answer(text, reply_markup=markup)

@dp.callback_query(lambda c: c.data and c.data.startswith("m:"))
async def on_callback(call: types.CallbackQuery):
    # Expected format: m:<game_id>:c:<cell_idx>  OR m:<game_id>:cashout  OR m:<game_id>:auto:<n>
    data = call.data.split(":")
    if len(data) < 3:
        await call.answer("Callback inválido", show_alert=True)
        return
    _, gid, cmd = data[:3]
    user_id = call.from_user.id

    # rate-limit
    if not rate_limit_check(user_id):
        await call.answer("Você está clicando rápido demais.")
        return

    # load game and verify ownership
    with SessionLocal() as db:
        game = db.query(Game).filter_by(id=gid).first()
        if not game:
            await call.answer("Jogo não encontrado.", show_alert=True)
            return
        if game.user_id != user_id:
            await call.answer("Esse jogo pertence a outro usuário.", show_alert=True)
            return
        if game.state != "playing":
            await call.answer("Jogo já finalizado.", show_alert=True)
            return

        if cmd == "c":
            idx = int(data[3])
            result = reveal_cell(db, game, idx)
            if result["lost"]:
                # edit message revealing all
                markup = render_grid_markup(game, reveal_all=True)
                await bot.edit_message_text(f"💥 Você perdeu! Seed: <code>{game.server_seed}</code>", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
                await call.answer("Boom! Você perdeu.")
                return
            else:
                # safe cell opened
                markup = render_grid_markup(game)
                await bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)
                await call.answer("Casa aberta! Continue ou saque.")
                return
        elif cmd == "cashout":
            # compute payout and attempt atomic cashout
            payout = compute_cashout(db, game)
            # NOTE: implement actual credit to user balance / transaction record here
            markup = render_grid_markup(game, reveal_all=True)
            await bot.edit_message_text(f"💰 Você sacou: {payout} (Seed: <code>{game.server_seed}</code>)", chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)
            await call.answer("Saque efetuado.")
            return
        else:
            await call.answer("Comando desconhecido.")
            return
