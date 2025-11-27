# Estrutura do projeto (resumo)

- main.py           -> FastAPI app (webhooks, healthcheck)
- bot_worker.py     -> Entry script que inicia aiogram (worker) e mantem o bot vivo
- bot.py            -> Handlers e lógica de interação com Telegram (aiogram)
- mines_engine.py   -> Lógica do jogo: commit/reveal, geração de bombs, multiplicadores
- db.py             -> Conexão com SQLAlchemy e modelos
- models.py         -> ORM models (User, Game, Transaction)
- payments.py       -> Funções auxiliares para confirmar depósitos/saques via webhook
- utils.py          -> Helpers: rate-limit, hmac, logging
- migrations/       -> (opcional) para Alembic
