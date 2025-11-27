import os
from fastapi import FastAPI, Header, Request, HTTPException
from dotenv import load_dotenv
import hmac, hashlib
from payments import handle_cryptopay_webhook
from utils import logger

load_dotenv()

app = FastAPI()

WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook/cryptopay")
CRYPTOPAY_SECRET = os.getenv("CRYPTOPAY_SECRET", "")

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/webhook/cryptopay")
async def cryptopay_webhook(request: Request, x_signature: str | None = Header(None)):
    body = await request.body()
    if not CRYPTOPAY_SECRET:
        logger.warning("No CRYPTOPAY_SECRET configured; rejecting webhook")
        raise HTTPException(status_code=400, detail="webhook not configured")

    # verify HMAC-SHA256 signature (provider should sign body with secret)
    computed = hmac.new(CRYPTOPAY_SECRET.encode(), body, hashlib.sha256).hexdigest()
    if not x_signature or not hmac.compare_digest(computed, x_signature):
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=401, detail="invalid signature")

    payload = await request.json()
    await handle_cryptopay_webhook(payload)
    return {"ok": True}
