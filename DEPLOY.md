# Deploy: GitHub -> Render (Passo a passo)

1. Crie um repositório no GitHub e envie todos os arquivos deste projeto (commit & push).
2. No Render: crie um novo **Web Service** a partir do repositório GitHub.
   - Build command: `pip install -r requirements.txt`
   - Start command: `bash -lc "python bot_worker.py & uvicorn main:app --host 0.0.0.0 --port $PORT"`
3. Configure as Environment Variables (Environment / Secrets) no Render:
   - BOT_TOKEN (token do BotFather)
   - DATABASE_URL (Postgres provido pelo Render ou outro host)
   - WEBHOOK_HOST (ex: https://your-app.onrender.com)
   - WEBHOOK_PATH (ex: /webhook/cryptopay)
   - CRYPTOPAY_SECRET (secret do provedor de pagamento)
   - RANDOM_SECRET_KEY (seed para HMAC commit/reveal)
   - ADMIN_TELEGRAM_ID (seu id para comandos admin)
4. Configure o Webhook do CryptoPay / provedor para apontar para:
   `${WEBHOOK_HOST}${WEBHOOK_PATH}`
   Verifique que o provedor envia um header com a assinatura que você definiu em CRYPTOPAY_SECRET.
5. Antes de abrir para usuários reais:
   - Teste com uma conta pequena e verifique logs.
   - Execute stress tests locais.
   - Cheque reversões/rollback seguros (não é implementado por padrão).
