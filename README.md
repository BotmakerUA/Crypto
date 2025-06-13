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

Open `http://localhost:8000/status` to check the bot status.

`/indicators` returns the current indicator settings, and `/indicator/<name>`
can enable or disable a specific indicator by sending `{ "enabled": true }`.

`/features` lists feature flags like turbo mode or trailing stop. Use
`/feature/<name>` with `{ "enabled": false }` to toggle them at runtime.
