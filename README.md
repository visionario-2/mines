# Mines Telegram Bot (Telegram Inline Buttons, Render-ready)

Projeto exemplo de um bot de apostas *Mines* rodando 100% via bot Telegram (inline buttons) + FastAPI webhook para pagamentos.
Arquivos prontos para subir no GitHub e implantar no Render.

**Principais características**
- Jogo Mines via inline keyboard (edita a mesma mensagem)
- Commit-reveal (hash do server seed) para provably-fair
- Persistência via PostgreSQL (padrão) ou SQLite (desenvolvimento)
- Segurança básica: validação de callbacks, rate-limiting por usuário, logs, tratamento atômico de cashout
- Estrutura pensada para deployment no Render

Veja `DEPLOY.md` para passo a passo do GitHub -> Render.

