# Notas de Segurança e Melhores Práticas

1. **HMAC / assinatura de webhook**: sempre valide a assinatura do provedor antes de processar webhooks.
2. **Commit-Reveal**: nunca revele o `server_seed` antes do jogo terminar; apenas mostre o `commit_hash` no início. Revele o `server_seed` ao final para prover auditoria.
3. **Proteja o BOT_TOKEN**: nunca exponha o token em código ou logs. Use secrets no Render.
4. **Use PostgreSQL**: SQLite é útil para dev, mas para produção use PostgreSQL com backups.
5. **Transações atômicas**: implemente bloqueios/transactions ao efetuar cashout para evitar double-spend.
6. **Auditoria**: guarde os seeds, bomb_positions e resultados para cada jogo (readonly logs).
7. **Limites**: implemente limites por usuário (diário, por aposta).
8. **Monitoramento**: integre Sentry / logs e monitore comportamento anômalo.
