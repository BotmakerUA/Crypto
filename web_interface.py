"""Simple Flask web interface for controlling NapalmProBotV2."""

from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
from napalm2 import NapalmProBotV2

app = Flask(__name__)
CORS(app)

# Storage for user-specific bot instances
bots = {}

def get_bot(user_id):
    return bots.get(user_id)

def create_bot(user_id, settings):
    bot = NapalmProBotV2(
        user_id=user_id,
        telegram_token=settings.get('telegram_token'),
        telegram_chat_id=settings.get('telegram_chat_id'),
        symbol=settings.get('symbol'),
        timeframe=settings.get('timeframe'),
        leverage=settings.get('leverage'),
        virtual_mode=settings.get('virtual', True),
    )
    bots[user_id] = bot
    return bot

@app.route('/users')
def list_users():
    return jsonify(list(bots.keys()))

@app.route('/user/<user_id>', methods=['POST'])
def create_user(user_id):
    data = request.get_json(force=True) or {}
    bot = create_bot(user_id, data)
    return jsonify({'user_id': user_id})

@app.route('/user/<user_id>/status')
def user_status(user_id):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    return jsonify({
        'running': bot.is_running,
        'symbol': bot.current_symbol,
        'timeframe': bot.current_timeframe,
        'indicators': bot.indicator_settings,
        'features': bot.feature_flags,
    })

@app.route('/user/<user_id>/start', methods=['POST'])
def user_start(user_id):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    if not bot.is_running:
        bot.is_running = True
        Thread(target=bot.run).start()
    return jsonify({'running': bot.is_running})

@app.route('/user/<user_id>/stop', methods=['POST'])
def user_stop(user_id):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    bot.is_running = False
    return jsonify({'running': bot.is_running})

@app.route('/user/<user_id>/features')
def user_features(user_id):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    return jsonify(bot.feature_flags)

@app.route('/user/<user_id>/feature/<name>', methods=['POST'])
def user_set_feature(user_id, name):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json(force=True)
    value = bool(data.get('enabled', True))
    if name in bot.feature_flags:
        if name == 'turbo_mode' and value != bot.turbo_mode:
            bot.toggle_turbo_mode()
        elif name == 'aggressive_mode' and value != (bot.aggressive_multiplier > 1.0):
            bot.toggle_aggressive_mode()
        elif name == 'trailing_stop' and value != bot.trailing_stop_enabled:
            bot.toggle_trailing_stop()
        elif name == 'machine_learning':
            bot.set_machine_learning(value)
        bot.feature_flags[name] = value
        return jsonify({name: bot.feature_flags[name]})
    return jsonify({'error': 'unknown feature'}), 400

@app.route('/user/<user_id>/indicators')
def user_indicators(user_id):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    return jsonify(bot.indicator_settings)

@app.route('/user/<user_id>/indicator/<name>', methods=['POST'])
def user_set_indicator(user_id, name):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    data = request.get_json(force=True)
    value = bool(data.get('enabled', True))
    if name in bot.indicator_settings:
        bot.indicator_settings[name] = value
        return jsonify({name: bot.indicator_settings[name]})
    return jsonify({'error': 'unknown indicator'}), 400

@app.route('/user/<user_id>/config', methods=['GET', 'POST'])
def user_config(user_id):
    bot = get_bot(user_id)
    if not bot:
        return jsonify({'error': 'not found'}), 404
    if request.method == 'POST':
        data = request.get_json(force=True)
        if 'symbol' in data:
            bot.current_symbol = data['symbol']
        if 'timeframe' in data:
            bot.current_timeframe = data['timeframe']
        if 'leverage' in data:
            bot.current_leverage = data['leverage']
        return jsonify({'updated': True})
    return jsonify({
        'symbol': bot.current_symbol,
        'timeframe': bot.current_timeframe,
        'leverage': bot.current_leverage,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
