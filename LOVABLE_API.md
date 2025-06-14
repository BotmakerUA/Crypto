# Lovable API Integration

The Flask server in `web_interface.py` exposes HTTP endpoints that the Lovable interface can call to manage each user's bot instance.

## Setup
1. Install requirements:
   ```bash
   pip install Flask Flask-Cors scikit-learn
   ```
2. Run the server:
   ```bash
   python web_interface.py
   ```
3. Send requests from the Lovable frontend to the server URL (default `http://localhost:8000`).

`web_interface.py` enables CORS so browser-based clients can call the API directly.

## Core Endpoints
- `GET /users` – list active user IDs.
- `POST /user/<id>` – create a bot for a user. JSON fields:
  `telegram_token`, `telegram_chat_id`, `symbol`, `timeframe`, `leverage`, `virtual`.
- `GET /user/<id>/status` – current config and feature state.
- `POST /user/<id>/start` – start trading for that user.
- `POST /user/<id>/stop` – stop trading.
- `GET /user/<id>/config` – fetch symbol/timeframe/leverage.
- `POST /user/<id>/config` – update any of those fields.
- `GET /user/<id>/features` – view feature flags.
- `POST /user/<id>/feature/<name>` – enable/disable a feature. Body: `{ "enabled": true }`.
- `GET /user/<id>/indicators` – view indicator flags.
- `POST /user/<id>/indicator/<name>` – toggle an indicator. Body: `{ "enabled": true }`.
- `GET /user/<id>/settings` – fetch full configuration including features and indicators.
- `POST /user/<id>/settings` – update any combination of options.

## Example
```bash
curl -X POST http://localhost:8000/user/alice \
     -H "Content-Type: application/json" \
     -d '{"telegram_token":"TOKEN","telegram_chat_id":123456}'
```

Use similar calls from Lovable to control each bot.

