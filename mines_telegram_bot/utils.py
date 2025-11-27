import time, hmac, hashlib, logging, os
from dotenv import load_dotenv
load_dotenv()

# Simple logger
logger = logging.getLogger("mines")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Rate-limiter (in-memory simple)
_RATE = {}
RATE_WINDOW = 1.0  # seconds
RATE_MAX = 3

def rate_limit_check(user_id:int):
    now = time.time()
    arr = _RATE.get(user_id, [])
    # drop old
    arr = [t for t in arr if now - t < RATE_WINDOW]
    if len(arr) >= RATE_MAX:
        return False
    arr.append(now)
    _RATE[user_id] = arr
    return True

def ensure_user(db, tg_user):
    # create or get user
    from models import User
    u = db.query(User).filter_by(telegram_id=str(tg_user.id)).first()
    if not u:
        u = User(telegram_id=str(tg_user.id), balance=0)
        db.add(u); db.commit(); db.refresh(u)
    return u
