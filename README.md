# Crypto

This repository contains **NapalmProBotV2**, a crypto trading bot.

## Features

- Automated trading logic with trend filters and adaptive stops.
- Telegram integration for notifications and commands.
- New `web_interface.py` provides a basic Flask web server to start/stop the bot
  and toggle the trend filter or individual indicators.
- New `ml_agent.py` records trade outcomes and trains a logistic regression
  model. The bot uses the predicted probability to adjust signal strength.

## Running the web interface

Install requirements and start the server:

```bash
pip install Flask scikit-learn
python web_interface.py
```

Create a user bot via `POST /user/<id>` with JSON settings (symbol,
timeframe, telegram ids). Then manage each bot with the following endpoints:

- `GET /users` – list active user IDs
- `GET /user/<id>/status` – current state for a user
- `POST /user/<id>/start` / `POST /user/<id>/stop` – control trading
- `GET/POST /user/<id>/config` – fetch or update symbol/timeframe/leverage
- `GET /user/<id>/features` and `POST /user/<id>/feature/<name>` – toggle
  features like turbo or trailing stop
- `GET /user/<id>/indicators` and `POST /user/<id>/indicator/<name>` – manage
  indicator filters
