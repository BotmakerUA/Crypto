"""Simple Flask web interface for controlling NapalmProBotV2."""

from flask import Flask, request, jsonify
from threading import Thread
from napalm2 import NapalmProBotV2

app = Flask(__name__)

bot = NapalmProBotV2(virtual_mode=True)

@app.route('/status')
def status():
    return jsonify({'running': bot.is_running,
                    'trend_filter': bot.trend_filter.enabled,
                    'strategy': 'default',
                    'indicators': bot.indicator_settings,
                    'features': bot.feature_flags})

@app.route('/indicators')
def indicators():
    return jsonify(bot.indicator_settings)

@app.route('/indicator/<name>', methods=['POST'])
def set_indicator(name):
    data = request.get_json(force=True)
    value = bool(data.get('enabled', True))
    if name in bot.indicator_settings:
        bot.indicator_settings[name] = value
        return jsonify({name: bot.indicator_settings[name]})
    return jsonify({'error': 'unknown indicator'}), 400

@app.route('/trend_filter', methods=['POST'])
def set_trend_filter():
    data = request.get_json(force=True)
    enabled = bool(data.get('enabled', True))
    bot.trend_filter.enabled = enabled
    return jsonify({'trend_filter': bot.trend_filter.enabled})

@app.route('/features')
def features():
    return jsonify(bot.feature_flags)

@app.route('/feature/<name>', methods=['POST'])
def set_feature(name):
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

@app.route('/start', methods=['POST'])
def start_bot():
    if not bot.is_running:
        bot.is_running = True
        Thread(target=bot.run).start()
    return jsonify({'running': bot.is_running})

@app.route('/stop', methods=['POST'])
def stop_bot():
    bot.is_running = False
    return jsonify({'running': bot.is_running})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
