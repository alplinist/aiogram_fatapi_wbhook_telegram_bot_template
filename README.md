# aiogram_fatapi_wbhook_telegram_bot_template
This is aiogram(aiogram + FastAPi webhook) template


Install everything:
```bash
pip install -r requirements.txt
```

Run the application with uvicorn:
```bash
uvicorn api.main:app --reload
```

### Project structure

```
bot/          - Telegram bot logic
  bot.py      - Bot initialization
  fsm/        - FSM state definitions
  handlers/   - Message handlers
api/          - FastAPI backend
  main.py     - Application entrypoint
  deps.py     - Dependency utilities
  schemas.py  - Pydantic schemas
  routes/     - API routes
core/         - Shared configuration and services
```

### API overview

- `POST /api/register` – create or update a user
- `POST /api/orders` – create an order for a user
- `POST /api/orders/{tracking}` – update order status/weight
- `GET /api/orders/{user_id}` – list user orders
- `GET /api/addresses/{user_id}` – list user addresses
- `POST /api/addresses` – add a new address

