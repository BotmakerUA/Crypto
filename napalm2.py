#!/usr/bin/env python3
"""
🔥🔥🔥 NAPALM PRO BOT V2 - РЕВОЛЮЦИОННЫЕ УЛУЧШЕНИЯ 🔥🔥🔥

КЛЮЧЕВЫЕ ИСПРАВЛЕНИЯ:
✅ Pullback Entry вместо Late Entry
✅ Исправленный трейлинг стоп  
✅ Трендовый фильтр с EMA
✅ RSI и объемные фильтры
✅ Адаптивные стопы на основе ATR
✅ Улучшенная статистика
"""

import ccxt
import pandas as pd
import numpy as np
import time
import json
import logging
import requests
import threading
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import random
from ml_agent import MachineLearningAgent

# Импорт из config_fixed.py
try:
    from config_fixed import *
except ImportError:
    # Fallback константы если config_fixed.py не найден
    API_KEY = "YOUR_API_KEY"
    API_SECRET = "YOUR_API_SECRET"
    TESTNET_MODE = True
    SYMBOL = "BTCUSDT"
    TIMEFRAME = "1m"
    LEVERAGE = 10
    START_BALANCE = 100.0
    BRICK_SIZE = 0.005
    TELEGRAM_TOKEN = "YOUR_TELEGRAM_TOKEN"
    TELEGRAM_CHAT_ID = 0
    INDICATOR_SETTINGS = {
        'use_rsi': True,
        'use_bollinger': True,
        'use_volume_filter': True,
        'use_macd': False,
    }
    FEATURE_FLAGS = {
        'machine_learning': True,
        'trailing_stop': True,
        'turbo_mode': False,
        'aggressive_mode': False,
    }

# 🔥 НОВЫЕ КОНСТАНТЫ V2 🔥

# Напалмовые фракции для умного мартингейла
NAPALM_FRACTIONS = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64]  # 2%, 4%, 8%, 16%, 32%, 64%

# Настройки трендового фильтра
TREND_FILTER_SETTINGS = {
    'enabled': True,
    'ema_period': 20,
    'block_against_trend': True,
    'enhance_with_trend': True,
    'neutral_zone_trading': True,
    'min_trend_confidence': 50,
    'max_enhancement': 0.5
}

# Режимы трендового фильтра
TREND_MODES = {
    'conservative': {
        'block_against_trend': True,
        'enhance_with_trend': False,
        'neutral_zone_trading': True,
        'min_trend_confidence': 70
    },
    'moderate': {
        'block_against_trend': True,
        'enhance_with_trend': True,
        'neutral_zone_trading': True,
        'min_trend_confidence': 50
    },
    'aggressive': {
        'block_against_trend': False,
        'enhance_with_trend': True,
        'neutral_zone_trading': True,
        'min_trend_confidence': 30
    }
}

# Текущий режим тренда
CURRENT_TREND_MODE = 'moderate'

# Мотивационные сообщения
NAPALM_MESSAGES = {
    'startup': [
        "💥 НАПАЛМ V2 ГОТОВ СЖЕЧЬ РЫНКИ!",
        "🚀 РЕВОЛЮЦИОННАЯ ВЕРСИЯ ЗАПУЩЕНА!",
        "⚡ PULLBACK СТРАТЕГИЯ АКТИВИРОВАНА!",
        "🔥 ТРЕНДОВЫЙ ФИЛЬТР В БОЕВОЙ ГОТОВНОСТИ!"
    ],
    'win': [
        "💥 НАПАЛМ ВЗОРВАЛ ЦЕЛЬ!",
        "🎯 ТОЧНОЕ ПОПАДАНИЕ!",
        "🔥 ПРИБЫЛЬ ЗАХВАЧЕНА!",
        "⚡ PULLBACK СРАБОТАЛ!"
    ],
    'loss': [
        "🛡 ЗАЩИТА СРАБОТАЛА!",
        "⚔️ БОЙЦЫ НЕ СДАЮТСЯ!",
        "💪 НАПАЛМ ПЕРЕГРУППИРУЕТСЯ!",
        "🔄 ГОТОВИМСЯ К КОНТРАТАКЕ!"
    ]
}

@dataclass
class TradeResult:
    """Детальная информация о сделке"""
    entry_price: float
    exit_price: float
    quantity: float
    side: str
    pnl: float
    pnl_percent: float
    commission: float
    net_pnl: float
    hold_time: timedelta
    signal_strength: float
    signal_reason: str

class TrendFilter:
    """Трендовый фильтр для улучшения сигналов"""
    
    def __init__(self, settings):
        self.settings = settings
        self.enabled = settings.get('enabled', True)
        self.ema_period = settings.get('ema_period', 20)
        self.block_against_trend = settings.get('block_against_trend', True)
        self.enhance_with_trend = settings.get('enhance_with_trend', True)
        self.neutral_zone_trading = settings.get('neutral_zone_trading', True)
        self.min_trend_confidence = settings.get('min_trend_confidence', 50)
        self.max_enhancement = settings.get('max_enhancement', 0.5)
        
    def analyze_trend(self, df):
        """Анализ тренда на основе EMA"""
        try:
            if not self.enabled or len(df) < self.ema_period + 5:
                return {
                    'trend_direction': 'neutral',
                    'trend_strength': 0,
                    'trend_confidence': 0
                }
            
            current_price = df['close'].iloc[-1]
            current_ema = df['ema_20'].iloc[-1] if 'ema_20' in df.columns else current_price
            prev_ema = df['ema_20'].iloc[-5] if len(df) > 5 else current_ema
            
            ema_direction = 1 if current_ema > prev_ema else -1
            price_distance = ((current_price - current_ema) / current_ema) * 100
            
            if price_distance > 0.5 and ema_direction > 0:
                trend_direction = 'bullish'
            elif price_distance < -0.5 and ema_direction < 0:
                trend_direction = 'bearish'
            else:
                trend_direction = 'neutral'
            
            trend_strength = min(100, abs(price_distance) * 20)
            trend_confidence = trend_strength
            
            return {
                'trend_direction': trend_direction,
                'trend_strength': trend_strength,
                'trend_confidence': trend_confidence,
                'price_vs_ema': price_distance,
                'ema_slope': ema_direction
            }
            
        except Exception as e:
            logging.error(f"Ошибка анализа тренда: {e}")
            return {
                'trend_direction': 'neutral',
                'trend_strength': 0,
                'trend_confidence': 0
            }
    
    def filter_signal(self, signal, trend_direction, trend_strength):
        """Фильтрация сигнала через тренд"""
        if not self.enabled:
            return {'blocked': False, 'enhanced': False, 'multiplier': 1.0, 'reason': ''}
        
        if self.block_against_trend and trend_strength > self.min_trend_confidence:
            if signal == 'buy' and trend_direction == 'bearish':
                return {
                    'blocked': True,
                    'enhanced': False,
                    'multiplier': 1.0,
                    'reason': f'LONG blocked by bearish trend ({trend_strength:.0f}%)'
                }
            elif signal == 'sell' and trend_direction == 'bullish':
                return {
                    'blocked': True,
                    'enhanced': False,
                    'multiplier': 1.0,
                    'reason': f'SHORT blocked by bullish trend ({trend_strength:.0f}%)'
                }
        
        enhanced = False
        multiplier = 1.0
        
        if self.enhance_with_trend and trend_strength > self.min_trend_confidence:
            if (signal == 'buy' and trend_direction == 'bullish') or \
               (signal == 'sell' and trend_direction == 'bearish'):
                enhanced = True
                enhancement = (trend_strength / 100) * self.max_enhancement
                multiplier = 1.0 + enhancement
        
        return {
            'blocked': False,
            'enhanced': enhanced,
            'multiplier': multiplier,
            'reason': f'Enhanced by {trend_direction} trend' if enhanced else ''
        }
    
    def get_signal_multiplier(self, trend_direction, trend_strength):
        """Получить множитель для размера позиции"""
        if not self.enabled or trend_direction == 'neutral':
            return 1.0
        
        if trend_strength > 70:
            return 1.2
        elif trend_strength > 50:
            return 1.1
        else:
            return 1.0

class NapalmProBotV2:
    def __init__(self, user_id='default', telegram_token=None, telegram_chat_id=None,
                 symbol=None, timeframe=None, leverage=None,
                 virtual_mode=True):
        # 🎮 Режим торговли
        self.user_id = user_id
        self.telegram_token = telegram_token or TELEGRAM_TOKEN
        self.telegram_chat_id = telegram_chat_id or TELEGRAM_CHAT_ID

        self.virtual_mode = virtual_mode
        self.virtual_balance = START_BALANCE
        
        # 🔥 УЛУЧШЕННЫЕ АДАПТИВНЫЕ ПАРАМЕТРЫ
        self.adaptive_brick_size = BRICK_SIZE
        self.base_position_size = 0.02
        self.aggressive_multiplier = 1.0
        self.volatility_window = 20
        
        # 💰 НАПАЛМОВЫЙ МАРТИНГЕЙЛ
        self.napalm_fractions = NAPALM_FRACTIONS
        self.martingale_index = 0
        self.recovery_mode = False
        
        # 📊 УЛУЧШЕННЫЙ ТРЕЙЛИНГ И РИСК-МЕНЕДЖМЕНТ
        self.trailing_stop_enabled = True
        self.dynamic_stops_enabled = True
        self.min_profit_for_trailing = 0.5
        
        # 🎯 СОСТОЯНИЕ
        self.current_position = None
        self.position_history = []
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.turbo_mode = False
        self.last_brick_time = None
        
        # 🎯 НОВЫЙ ТРЕНДОВЫЙ ФИЛЬТР
        self.trend_filter = TrendFilter(TREND_FILTER_SETTINGS)

        # 📈 Machine learning helper
        self.ml_agent = MachineLearningAgent()

        # ⚙️ Индикаторы
        self.indicator_settings = INDICATOR_SETTINGS.copy()

        # 🔧 Флаги функций
        self.feature_flags = FEATURE_FLAGS.copy()
        self.use_ml = self.feature_flags.get('machine_learning', True)
        self.trailing_stop_enabled = self.feature_flags.get('trailing_stop', True)
        self.turbo_mode = self.feature_flags.get('turbo_mode', False)
        if self.feature_flags.get('aggressive_mode', False):
            self.aggressive_multiplier = 2.0
        
        # 📈 РАСШИРЕННЫЕ РЫНОЧНЫЕ ДАННЫЕ
        self.market_conditions = {
            'volatility': 0,
            'trend_direction': 'neutral',
            'trend_strength': 0,
            'rsi': 50,
            'volume_ratio': 1.0,
            'bb_position': 0.5,
            'last_update': None
        }
        
        # 💹 УЛУЧШЕННАЯ СТАТИСТИКА
        self.stats = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'total_pnl': 0,
            'total_commission': 0,
            'max_win': 0,
            'max_loss': 0,
            'avg_win': 0,
            'avg_loss': 0,
            'sharpe_ratio': 0,
            'profit_factor': 0,
            'win_rate': 0,
            'expectancy': 0,
            'max_drawdown': 0,
            'current_drawdown': 0,
            'peak_balance': START_BALANCE,
            'start_time': datetime.now(),
            'session_high': START_BALANCE,
            'session_low': START_BALANCE,
            'trend_blocks': 0,
            'trend_enhancements': 0,
            'pullback_entries': 0,
            'momentum_entries': 0,
            'false_signals_blocked': 0
        }
        
        # Торговые параметры
        self.current_symbol = symbol or SYMBOL
        self.current_timeframe = timeframe or TIMEFRAME
        self.current_leverage = leverage or LEVERAGE
        self.is_running = True
        self.should_stop = False
        self.last_update_id = 0
        
        # Настройка логирования
        log_file = 'napalm_pro_v2.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        
        # Инициализация
        self.exchange = None
        self.init_exchange()
        self.init_telegram()
        
        # Запуск потоков
        self.command_thread = threading.Thread(target=self.telegram_command_handler, daemon=True)
        self.market_analyzer_thread = threading.Thread(target=self.market_analyzer, daemon=True)
        
        self.command_thread.start()
        self.market_analyzer_thread.start()

    def init_exchange(self):
        """Инициализация биржи"""
        try:
            self.exchange = ccxt.bybit({
                'apiKey': API_KEY,
                'secret': API_SECRET,
                'sandbox': TESTNET_MODE,
                'enableRateLimit': True,
                'options': {'defaultType': 'future'}
            })

            if not self.virtual_mode:
                try:
                    self.exchange.set_leverage(self.current_leverage, self.current_symbol)
                    logging.info(f"✅ Плечо установлено: x{self.current_leverage}")
                except Exception as e:
                    if "110043" in str(e):
                        logging.info("✅ Плечо уже установлено")

            mode = "🎮 ВИРТУАЛЬНЫЙ" if self.virtual_mode else "💰 РЕАЛЬНЫЙ"
            logging.info(f"✅ Exchange подключен в режиме: {mode}")

        except Exception as e:
            logging.error(f"❌ Ошибка подключения: {e}")
            raise

    def init_telegram(self):
        """Инициализация Telegram"""
        try:
            self.clear_old_messages()
            self.send_startup_message()
            logging.info("✅ Telegram инициализирован")
        except Exception as e:
            logging.error(f"❌ Ошибка Telegram: {e}")

    def clear_old_messages(self):
        """Очистка старых сообщений"""
        try:
            logging.info("🧹 Очистка старых сообщений...")
            url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
            params = {'timeout': 1}
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data['ok'] and data['result']:
                    last_update = data['result'][-1]
                    self.last_update_id = last_update['update_id']
                    
                    confirm_url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
                    confirm_params = {'offset': self.last_update_id + 1}
                    requests.get(confirm_url, params=confirm_params, timeout=5)
                    
                    logging.info(f"✅ Очищено до ID: {self.last_update_id}")
        except Exception as e:
            logging.warning(f"Ошибка очистки: {e}")

    def send_startup_message(self):
        """Улучшенное стартовое сообщение"""
        mode = "🎮 ВИРТУАЛЬНЫЙ" if self.virtual_mode else "💰 РЕАЛЬНЫЙ"
        startup_msg = random.choice(NAPALM_MESSAGES['startup'])
        
        message = f"""
🔥🔥🔥 <b>NAPALM PRO BOT V2 ЗАПУЩЕН!</b> 🔥🔥🔥

{startup_msg}

🎯 <b>Режим:</b> {mode}
🪙 <b>Символ:</b> {self.current_symbol}
💰 <b>Баланс:</b> ${START_BALANCE:.2f}
🎚 <b>Плечо:</b> x{self.current_leverage}

🚀 <b>РЕВОЛЮЦИОННЫЕ УЛУЧШЕНИЯ V2:</b>
✅ Pullback Entry стратегия
✅ Исправленный трейлинг стоп  
✅ Трендовый фильтр с EMA
✅ RSI и Bollinger Bands фильтры
✅ Динамические ATR стопы
✅ Напалмовый мартингейл до x64%

🎯 <b>ТРЕНДОВЫЙ ФИЛЬТР:</b>
• Режим: {CURRENT_TREND_MODE.upper()}
• EMA период: {self.trend_filter.ema_period}
• Блокировка против тренда: ✅
• Усиление по тренду: ✅

📊 <b>ТЕКУЩИЕ НАСТРОЙКИ:</b>
• Кирпич: ${self.adaptive_brick_size:.6f}
• Трейлинг: {"ВКЛ" if self.trailing_stop_enabled else "ВЫКЛ"}
• База позиции: {self.base_position_size*100}%

🎮 <b>КОМАНДЫ:</b>
/napalm - НАПАЛМОВАЯ статистика
/trend - Трендовый фильтр
/help - Все команды
/stop - Остановка

🎯 <b>ЦЕЛЬ: 344% ROI КАК В БЭКТЕСТЕ!</b>
💡 <b>Начните с виртуального режима для изучения!</b>

🔥 НАПАЛМ V2 ГОТОВ К БОЮ! 🔥
        """
        
        self.send_telegram_message(message)

    def send_telegram_message(self, message):
        """Отправка сообщения в Telegram"""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code != 200:
                logging.error(f"Ошибка Telegram: {response.text}")
                
        except Exception as e:
            logging.error(f"Ошибка отправки: {e}")

    def telegram_command_handler(self):
        """Обработчик команд Telegram"""
        while self.is_running:
            try:
                url = f"https://api.telegram.org/bot{self.telegram_token}/getUpdates"
                params = {
                    'offset': self.last_update_id + 1,
                    'timeout': 10,
                    'allowed_updates': ['message']
                }
                
                response = requests.get(url, params=params, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['ok'] and data['result']:
                        for update in data['result']:
                            self.last_update_id = update['update_id']
                            
                            if 'message' in update and 'text' in update['message']:
                                chat_id = update['message']['chat']['id']
                                text = update['message']['text'].strip().lower()
                                message_date = update['message']['date']
                                
                                current_time = int(time.time())
                                message_age = current_time - message_date
                                
                                if message_age > 60:
                                    continue
                                    
                                if chat_id == self.telegram_chat_id:
                                    logging.info(f"📨 Команда: {text}")
                                    self.process_enhanced_command(text)
                
                time.sleep(3)
                
            except Exception as e:
                logging.error(f"Ошибка команд: {e}")
                time.sleep(5)

    def process_enhanced_command(self, command):
        """Обработка улучшенных команд"""
        try:
            commands = {
                '/stop': self.handle_stop_command,
                '/napalm': self.send_napalm_performance_report,
                '/stats': self.send_napalm_performance_report,
                '/status': self.send_enhanced_status,
                '/balance': self.send_balance,
                '/position': self.send_position_info,
                '/reset': self.handle_reset_command,
                '/turbo': self.toggle_turbo_mode,
                '/real': self.switch_to_real_mode,
                '/virtual': self.switch_to_virtual_mode,
                '/aggressive': self.toggle_aggressive_mode,
                '/trailing': self.toggle_trailing_stop,
                '/report': self.send_last_trades_report,
                '/help': self.send_enhanced_help,
                '/trend': self.send_trend_status,
                '/trend_mode': self.cycle_trend_mode,
                '/trend_off': self.disable_trend_filter,
                '/trend_on': self.enable_trend_filter
            }
            
            handler = commands.get(command)
            if handler:
                handler()
            else:
                if command.startswith('/brick'):
                    self.set_brick_size(command)
                elif command.startswith('/tp'):
                    self.set_take_profit(command)
                elif command.startswith('/sl'):
                    self.set_stop_loss(command)
                else:
                    logging.info(f"Неизвестная команда: {command}")
                    
        except Exception as e:
            logging.error(f"Ошибка обработки команды: {e}")

    def market_analyzer(self):
        """Улучшенный анализатор рыночных условий"""
        while self.is_running:
            try:
                self.analyze_enhanced_market_conditions()
                self.adapt_strategy_v2()
                time.sleep(30)
            except Exception as e:
                logging.error(f"Ошибка анализа рынка: {e}")
                time.sleep(60)

    def analyze_enhanced_market_conditions(self):
        """Расширенный анализ рыночных условий"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.current_symbol, '5m', limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            
            df = self.calculate_technical_indicators(df)
            
            current_price = df['close'].iloc[-1]
            
            self.market_conditions.update({
                'volatility': df['volatility_percent'].iloc[-1],
                'rsi': df['rsi'].iloc[-1],
                'volume_ratio': df['volume_ratio'].iloc[-1],
                'bb_position': df['bb_position'].iloc[-1],
                'macd_hist': df['macd_hist'].iloc[-1],
                'last_update': datetime.now()
            })
            
            trend_info = self.trend_filter.analyze_trend(df)
            self.market_conditions.update(trend_info)
            
            logging.info(f"📊 Рынок: RSI {self.market_conditions['rsi']:.1f}, "
                        f"Волатильность {self.market_conditions['volatility']:.2f}%, "
                        f"Тренд: {self.market_conditions['trend_direction']} ({self.market_conditions['trend_strength']:.0f}%)")
            
        except Exception as e:
            logging.error(f"Ошибка анализа условий: {e}")

    def calculate_technical_indicators(self, df):
        """Расчет технических индикаторов"""
        def calculate_rsi(prices, period=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        
        df['ema_20'] = df['close'].ewm(span=20).mean()
        df['ema_50'] = df['close'].ewm(span=50).mean()
        df['rsi'] = calculate_rsi(df['close'])
        
        df['bb_middle'] = df['close'].rolling(20).mean()
        bb_std = df['close'].rolling(20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift()),
                abs(df['low'] - df['close'].shift())
            )
        )
        df['atr'] = df['tr'].rolling(14).mean()
        price = df['close'].iloc[-1]
        df['volatility_percent'] = (df['atr'] / price) * 100
        
        df['volume_ma'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']

        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        return df

    def adapt_strategy_v2(self):
        """Улучшенная адаптация стратегии"""
        volatility = self.market_conditions['volatility']
        trend_direction = self.market_conditions['trend_direction']
        trend_strength = self.market_conditions['trend_strength']
        
        if volatility > 2.0:
            self.adaptive_brick_size = BRICK_SIZE * 1.5
            self.aggressive_multiplier = 1.3
        elif volatility < 0.5:
            self.adaptive_brick_size = BRICK_SIZE * 0.8
            self.aggressive_multiplier = 1.8
        else:
            self.adaptive_brick_size = BRICK_SIZE
            self.aggressive_multiplier = 1.0
            
        if trend_direction != 'neutral' and trend_strength > 60:
            self.aggressive_multiplier *= 1.2
        
        if self.consecutive_losses >= 3:
            self.recovery_mode = True
            self.aggressive_multiplier *= 1.5
        elif self.consecutive_wins >= 2 and self.recovery_mode:
            self.recovery_mode = False

    def get_renko_data(self):
        """Получение данных для Renko"""
        try:
            ohlcv = self.exchange.fetch_ohlcv(self.current_symbol, self.current_timeframe, limit=240)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logging.error(f"Ошибка получения данных: {e}")
            return None

    def build_smart_renko_v2(self, df):
        """Умные Renko кирпичи V2"""
        try:
            bricks = []
            current_atr = df['atr'].iloc[-1] if 'atr' in df.columns else self.adaptive_brick_size
            current_price = df['close'].iloc[-1]
            
            atr_based_size = current_atr * 2
            percent_based_size = current_price * 0.008
            adaptive_size = max(min(atr_based_size, percent_based_size), self.adaptive_brick_size * 0.5)
            
            brick_size = adaptive_size
            current_brick_price = df.iloc[0]['close']
            
            for _, row in df.iterrows():
                high, low = row['high'], row['low']
                timestamp = row['timestamp']
                volume = row['volume']
                rsi = row.get('rsi', 50)
                volume_ratio = row.get('volume_ratio', 1.0)
                
                # Движение вверх
                while high >= current_brick_price + brick_size:
                    current_brick_price += brick_size
                    
                    volume_strength = min(2.0, volume_ratio)
                    rsi_strength = 1.0
                    
                    if not pd.isna(rsi):
                        if rsi < 30:
                            rsi_strength = 1.5
                        elif rsi > 70:
                            rsi_strength = 0.6
                    
                    bricks.append({
                        'timestamp': timestamp,
                        'open': current_brick_price - brick_size,
                        'close': current_brick_price,
                        'direction': 'up',
                        'volume': volume,
                        'strength': volume_strength * rsi_strength,
                        'rsi': rsi,
                        'size': brick_size
                    })

                # Движение вниз
                while low <= current_brick_price - brick_size:
                    current_brick_price -= brick_size
                    
                    volume_strength = min(2.0, volume_ratio)
                    rsi_strength = 1.0
                    
                    if not pd.isna(rsi):
                        if rsi > 70:
                            rsi_strength = 1.5
                        elif rsi < 30:
                            rsi_strength = 0.6
                    
                    bricks.append({
                        'timestamp': timestamp,
                        'open': current_brick_price + brick_size,
                        'close': current_brick_price,
                        'direction': 'down',
                        'volume': volume,
                        'strength': volume_strength * rsi_strength,
                        'rsi': rsi,
                        'size': brick_size
                    })

            return bricks
        except Exception as e:
            logging.error(f"Ошибка построения Renko: {e}")
            return []

    def has_new_brick(self, bricks):
        """Проверка новых кирпичей"""
        if not bricks:
            return False

        last_brick = bricks[-1]

        if self.last_brick_time is None or last_brick['timestamp'] > self.last_brick_time:
            self.last_brick_time = last_brick['timestamp']
            return True

        return False

    def analyze_revolutionary_signals(self, bricks, df):
        """🔥 РЕВОЛЮЦИОННАЯ ЛОГИКА СИГНАЛОВ V2 🔥"""
        if len(bricks) < 5:
            return None, 0, "Недостаточно кирпичей"
        
        current_price = df['close'].iloc[-1]
        current_rsi = df['rsi'].iloc[-1] if 'rsi' in df.columns else 50
        current_bb_pos = df['bb_position'].iloc[-1] if 'bb_position' in df.columns else 0.5
        volume_ratio = df['volume_ratio'].iloc[-1] if 'volume_ratio' in df.columns else 1.0
        macd_hist = df['macd_hist'].iloc[-1] if 'macd_hist' in df.columns else 0

        use_rsi = self.indicator_settings.get('use_rsi', True)
        use_bb = self.indicator_settings.get('use_bollinger', True)
        use_vol = self.indicator_settings.get('use_volume_filter', True)
        use_macd = self.indicator_settings.get('use_macd', False)
        
        last_5 = bricks[-5:]
        last_3 = bricks[-3:]
        
        signal = None
        strength = 0
        reason = ""
        
        # PULLBACK ENTRY СТРАТЕГИЯ
        down_count = 0
        for brick in reversed(last_3[:-1]):
            if brick['direction'] == 'down':
                down_count += 1
            else:
                break
        
        rsi_ok_long = 20 < current_rsi < 65 if use_rsi else True
        bb_ok_long = current_bb_pos < 0.8 if use_bb else True
        vol_ok = volume_ratio > 0.8 if use_vol else True
        macd_ok_long = macd_hist > 0 if use_macd else True

        if (down_count >= 2 and
            last_3[-1]['direction'] == 'up' and
            rsi_ok_long and bb_ok_long and vol_ok and macd_ok_long):
            
            signal = 'buy'
            strength = 0.75
            reason = "Pullback Long Entry"
            self.stats['pullback_entries'] += 1
            
            if current_rsi < 40:
                strength += 0.15
            if current_bb_pos < 0.3:
                strength += 0.1
        
        up_count = 0
        for brick in reversed(last_3[:-1]):
            if brick['direction'] == 'up':
                up_count += 1
            else:
                break
        
        rsi_ok_short = 35 < current_rsi < 80 if use_rsi else True
        bb_ok_short = current_bb_pos > 0.2 if use_bb else True
        if use_vol:
            vol_ok_short = volume_ratio > 0.8
        else:
            vol_ok_short = True
        macd_ok_short = macd_hist < 0 if use_macd else True

        if (up_count >= 2 and
            last_3[-1]['direction'] == 'down' and
            rsi_ok_short and bb_ok_short and vol_ok_short and macd_ok_short):
            
            signal = 'sell'
            strength = 0.75
            reason = "Pullback Short Entry"
            self.stats['pullback_entries'] += 1
            
            if current_rsi > 60:
                strength += 0.15
            if current_bb_pos > 0.7:
                strength += 0.1

        # MOMENTUM ENTRY (резервная)
        if not signal:
            up_sequence = 0
            for brick in reversed(last_5):
                if brick['direction'] == 'up':
                    up_sequence += 1
                else:
                    break
            
            rsi_mom_long = current_rsi < 70 if use_rsi else True
            bb_mom_long = current_bb_pos < 0.9 if use_bb else True
            vol_mom_long = volume_ratio > 1.0 if use_vol else True
            macd_mom_long = macd_hist > 0 if use_macd else True

            if (up_sequence >= 3 and
                rsi_mom_long and bb_mom_long and vol_mom_long and macd_mom_long):
                
                signal = 'buy'
                strength = 0.5 + (up_sequence * 0.05)
                reason = f"Momentum Long ({up_sequence} UP)"
                self.stats['momentum_entries'] += 1
            
            down_sequence = 0
            for brick in reversed(last_5):
                if brick['direction'] == 'down':
                    down_sequence += 1
                else:
                    break
            
            rsi_mom_short = current_rsi > 30 if use_rsi else True
            bb_mom_short = current_bb_pos > 0.1 if use_bb else True
            vol_mom_short = volume_ratio > 1.0 if use_vol else True
            macd_mom_short = macd_hist < 0 if use_macd else True

            if (down_sequence >= 3 and
                rsi_mom_short and bb_mom_short and vol_mom_short and macd_mom_short):
                
                signal = 'sell'
                strength = 0.5 + (down_sequence * 0.05)
                reason = f"Momentum Short ({down_sequence} DOWN)"
                self.stats['momentum_entries'] += 1
        
        # ФИЛЬТРЫ БЛОКИРОВКИ
        if signal:
            if use_rsi:
                if signal == 'buy' and current_rsi > 75:
                    self.stats['false_signals_blocked'] += 1
                    return None, 0, f"LONG blocked: RSI={current_rsi:.1f} overbought"

                if signal == 'sell' and current_rsi < 25:
                    self.stats['false_signals_blocked'] += 1
                    return None, 0, f"SHORT blocked: RSI={current_rsi:.1f} oversold"

            if use_bb:
                if signal == 'buy' and current_bb_pos > 0.95:
                    self.stats['false_signals_blocked'] += 1
                    return None, 0, f"LONG blocked: BB position={current_bb_pos:.2f}"

                if signal == 'sell' and current_bb_pos < 0.05:
                    self.stats['false_signals_blocked'] += 1
                    return None, 0, f"SHORT blocked: BB position={current_bb_pos:.2f}"
            
            # ТРЕНДОВЫЙ ФИЛЬТР
            trend_result = self.trend_filter.filter_signal(
                signal, 
                self.market_conditions['trend_direction'],
                self.market_conditions['trend_strength']
            )
            
            if trend_result['blocked']:
                self.stats['trend_blocks'] += 1
                return None, 0, f"Signal blocked by trend filter: {trend_result['reason']}"
            
            if trend_result['enhanced']:
                strength = min(strength * trend_result['multiplier'], 1.0)
                reason += f" + Trend Enhanced ({trend_result['multiplier']:.1f}x)"
                self.stats['trend_enhancements'] += 1
        
        if signal:
            features = [
                self.market_conditions['trend_strength'],
                self.market_conditions['rsi'],
                self.market_conditions['volatility']
            ]
            if use_macd:
                features.append(macd_hist)
            if self.use_ml:
                prob = self.ml_agent.predict(features)
                strength *= 0.5 + 0.5 * prob
                reason += f" + ML {prob:.2f}"

        strength = min(strength, 1.0)
        return signal, strength, reason

    def calculate_enhanced_position_size(self, signal_strength, signal_reason):
        """Улучшенный расчет размера позиции"""
        try:
            balance = self.virtual_balance if self.virtual_mode else self.exchange.fetch_balance()['USDT']['free']
            
            fraction = self.napalm_fractions[min(self.martingale_index, len(self.napalm_fractions)-1)]
            signal_mult = 0.5 + (signal_strength * 0.5)
            
            signal_type_mult = 1.0
            if "Pullback" in signal_reason:
                signal_type_mult = 1.2
            elif "Momentum" in signal_reason:
                signal_type_mult = 0.9
                
            trend_mult = self.trend_filter.get_signal_multiplier(
                self.market_conditions['trend_direction'],
                self.market_conditions['trend_strength']
            )
            
            aggression_mult = self.aggressive_multiplier
            turbo_mult = 1.5 if self.turbo_mode else 1.0
            
            final_fraction = fraction * signal_mult * signal_type_mult * trend_mult * aggression_mult * turbo_mult
            final_fraction = min(final_fraction, 1.0)
            
            risk_amount = balance * final_fraction
            current_price = self.get_current_price()
            quantity = (risk_amount * self.current_leverage) / current_price
            
            return round(quantity, 6)
            
        except Exception as e:
            logging.error(f"Ошибка расчета позиции: {e}")
            return 0

    def calculate_dynamic_stops_v2(self, df, signal, entry_price, signal_strength):
        """Динамические стопы V2 с ATR и адаптацией"""
        try:
            current_atr = df['atr'].iloc[-1] if 'atr' in df.columns else entry_price * 0.02
            current_rsi = df['rsi'].iloc[-1] if 'rsi' in df.columns else 50
            
            base_stop_mult = 2.0
            base_tp_mult = 3.0
            
            signal_adjustment = 0.8 + (signal_strength * 0.4)
            
            rsi_adjustment = 1.0
            if signal == 'buy':
                if current_rsi < 35:
                    rsi_adjustment = 1.3
                elif current_rsi > 60:
                    rsi_adjustment = 0.8
            else:
                if current_rsi > 65:
                    rsi_adjustment = 1.3
                elif current_rsi < 40:
                    rsi_adjustment = 0.8
            
            stop_distance = current_atr * base_stop_mult * signal_adjustment
            tp_distance = current_atr * base_tp_mult * signal_adjustment * rsi_adjustment
            
            if signal == 'buy':
                stop_loss = entry_price - stop_distance
                take_profit = entry_price + tp_distance
            else:
                stop_loss = entry_price + stop_distance
                take_profit = entry_price - tp_distance
            
            return {
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'atr_used': current_atr,
                'stop_distance': stop_distance,
                'tp_distance': tp_distance,
                'stop_percent': (stop_distance / entry_price) * 100,
                'tp_percent': (tp_distance / entry_price) * 100,
                'risk_reward': tp_distance / stop_distance
            }
            
        except Exception as e:
            logging.error(f"Ошибка расчета стопов: {e}")
            stop_percent = 2.0
            tp_percent = 3.0
            
            if signal == 'buy':
                return {
                    'stop_loss': entry_price * (1 - stop_percent/100),
                    'take_profit': entry_price * (1 + tp_percent/100),
                    'stop_percent': stop_percent,
                    'tp_percent': tp_percent,
                    'risk_reward': tp_percent / stop_percent
                }
            else:
                return {
                    'stop_loss': entry_price * (1 + stop_percent/100),
                    'take_profit': entry_price * (1 - tp_percent/100),
                    'stop_percent': stop_percent,
                    'tp_percent': tp_percent,
                    'risk_reward': tp_percent / stop_percent
                }

    def execute_trade_with_enhanced_stops(self, signal, quantity, signal_strength, signal_reason):
        """Исполнение сделки с улучшенными стопами"""
        try:
            current_price = self.get_current_price()
            if not current_price:
                return False
                
            df = self.get_renko_data()
            if df is None:
                return False
                
            df = self.calculate_technical_indicators(df)
            stops = self.calculate_dynamic_stops_v2(df, signal, current_price, signal_strength)
            
            commission = quantity * current_price * 0.0006
            
            self.current_position = {
                'side': signal,
                'quantity': quantity,
                'entry_price': current_price,
                'stop_loss': stops['stop_loss'],
                'take_profit': stops['take_profit'],
                'trailing_stop': None,
                'highest_price': current_price if signal == 'buy' else None,
                'lowest_price': current_price if signal == 'sell' else None,
                'commission_open': commission,
                'time': datetime.now(),
                'signal_strength': signal_strength,
                'signal_reason': signal_reason,
                'stops_info': stops,
                'virtual': self.virtual_mode,
                'atr_at_entry': stops.get('atr_used', current_price * 0.02)
            }
            
            if self.virtual_mode:
                self.stats['total_trades'] += 1
            else:
                order = self.exchange.create_market_order(
                    symbol=self.current_symbol,
                    side=signal,
                    amount=quantity
                )
                self.current_position['order_id'] = order['id']
                self.stats['total_trades'] += 1
            
            self.send_enhanced_trade_notification('open')
            return True
            
        except Exception as e:
            logging.error(f"Ошибка исполнения: {e}")
            return False

    def improved_trailing_logic_v2(self, position, current_price, df):
        """ИСПРАВЛЕННАЯ логика трейлинг стопа V2"""
        if not position:
            return None
            
        entry_price = position['entry_price']
        side = position['side']
        current_atr = df['atr'].iloc[-1] if 'atr' in df.columns else position.get('atr_at_entry', entry_price * 0.02)
        
        if side == 'buy':
            current_pnl_percent = ((current_price - entry_price) / entry_price) * 100
        else:
            current_pnl_percent = ((entry_price - current_price) / entry_price) * 100
        
        if current_pnl_percent <= self.min_profit_for_trailing:
            return None
        
        base_distance = current_atr * 1.5
        
        if current_pnl_percent > 3.0:
            distance_mult = 1.0
        elif current_pnl_percent > 1.5:
            distance_mult = 1.2
        else:
            distance_mult = 1.5
            
        trailing_distance = base_distance * distance_mult
        
        if side == 'buy':
            new_trailing_stop = current_price - trailing_distance
            
            if position.get('trailing_stop') is None:
                return new_trailing_stop
            else:
                return max(position['trailing_stop'], new_trailing_stop)
                
        else:
            new_trailing_stop = current_price + trailing_distance
            
            if position.get('trailing_stop') is None:
                return new_trailing_stop
            else:
                return min(position['trailing_stop'], new_trailing_stop)

    def check_enhanced_position_stops(self):
        """Улучшенная проверка стоп-лоссов и тейк-профитов"""
        if not self.current_position:
            return
            
        current_price = self.get_current_price()
        if not current_price:
            return
            
        pos = self.current_position
        
        df = self.get_renko_data()
        if df is not None:
            df = self.calculate_technical_indicators(df)
            
            if pos['side'] == 'buy' and current_price > pos['highest_price']:
                pos['highest_price'] = current_price
            elif pos['side'] == 'sell' and current_price < pos['lowest_price']:
                pos['lowest_price'] = current_price
            
            if self.trailing_stop_enabled:
                new_trailing = self.improved_trailing_logic_v2(pos, current_price, df)
                if new_trailing:
                    pos['trailing_stop'] = new_trailing
        
        should_close = False
        close_reason = ""
        
        if pos['side'] == 'buy':
            if current_price <= pos['stop_loss']:
                should_close = True
                close_reason = "Stop Loss"
            elif current_price >= pos['take_profit']:
                should_close = True
                close_reason = "Take Profit"
            elif pos['trailing_stop'] and current_price <= pos['trailing_stop']:
                should_close = True
                close_reason = "Trailing Stop"
        else:
            if current_price >= pos['stop_loss']:
                should_close = True
                close_reason = "Stop Loss"
            elif current_price <= pos['take_profit']:
                should_close = True
                close_reason = "Take Profit"
            elif pos['trailing_stop'] and current_price >= pos['trailing_stop']:
                should_close = True
                close_reason = "Trailing Stop"
        
        if should_close:
            self.close_position_enhanced(current_price, close_reason)

    def close_position_enhanced(self, exit_price, reason="Signal"):
        """Закрытие позиции с улучшенным отчетом"""
        if not self.current_position:
            return
            
        pos = self.current_position
        
        if pos['side'] == 'buy':
            gross_pnl = (exit_price - pos['entry_price']) * pos['quantity']
        else:
            gross_pnl = (pos['entry_price'] - exit_price) * pos['quantity']
            
        commission_close = pos['quantity'] * exit_price * 0.0006
        total_commission = pos['commission_open'] + commission_close
        net_pnl = gross_pnl - total_commission
        
        pnl_percent = (net_pnl / (pos['entry_price'] * pos['quantity'])) * 100
        hold_time = datetime.now() - pos['time']
        
        trade_result = TradeResult(
            entry_price=pos['entry_price'],
            exit_price=exit_price,
            quantity=pos['quantity'],
            side=pos['side'],
            pnl=gross_pnl,
            pnl_percent=pnl_percent,
            commission=total_commission,
            net_pnl=net_pnl,
            hold_time=hold_time,
            signal_strength=pos['signal_strength'],
            signal_reason=pos['signal_reason']
        )
        
        if self.virtual_mode:
            self.virtual_balance += net_pnl
            
        self.update_enhanced_statistics(trade_result)
        
        self.position_history.append({
            'result': trade_result,
            'reason': reason,
            'time': datetime.now(),
            'stops_info': pos.get('stops_info', {}),
            'market_conditions': self.market_conditions.copy()
        })
        
        self.send_enhanced_trade_notification('close', trade_result, reason)
        self.current_position = None
        
        if net_pnl > 0:
            self.consecutive_wins += 1
            self.consecutive_losses = 0
            if self.martingale_index > 0:
                self.martingale_index = 0
                
            motivational = random.choice(NAPALM_MESSAGES['win'])
            self.send_telegram_message(f"🎉 {motivational}")
        else:
            self.consecutive_losses += 1
            self.consecutive_wins = 0
            self.martingale_index = min(self.martingale_index + 1, len(self.napalm_fractions) - 1)
            
            motivational = random.choice(NAPALM_MESSAGES['loss'])
            self.send_telegram_message(f"💪 {motivational}")
            
        if self.consecutive_wins >= 3 and not self.turbo_mode:
            self.turbo_mode = True
            self.send_telegram_message("⚡ ТУРБО РЕЖИМ АКТИВИРОВАН! 🔥🔥🔥")
        elif self.turbo_mode and self.consecutive_losses >= 2:
            self.turbo_mode = False
            self.send_telegram_message("❄️ Турбо режим отключен")

    def update_enhanced_statistics(self, trade_result: TradeResult):
        """Обновление улучшенной статистики"""
        self.stats['total_pnl'] += trade_result.net_pnl
        self.stats['total_commission'] += trade_result.commission
        
        if trade_result.net_pnl > 0:
            self.stats['winning_trades'] += 1
            self.stats['max_win'] = max(self.stats['max_win'], trade_result.net_pnl)
        else:
            self.stats['losing_trades'] += 1
            self.stats['max_loss'] = min(self.stats['max_loss'], trade_result.net_pnl)
            
        total_trades = self.stats['winning_trades'] + self.stats['losing_trades']
        
        if self.stats['winning_trades'] > 0:
            total_wins = sum(h['result'].net_pnl for h in self.position_history if h['result'].net_pnl > 0)
            self.stats['avg_win'] = total_wins / self.stats['winning_trades']
            
        if self.stats['losing_trades'] > 0:
            total_losses = sum(h['result'].net_pnl for h in self.position_history if h['result'].net_pnl < 0)
            self.stats['avg_loss'] = total_losses / self.stats['losing_trades']
            
        if total_trades > 0:
            self.stats['win_rate'] = (self.stats['winning_trades'] / total_trades) * 100
            
        if self.stats['avg_loss'] < 0 and self.stats['losing_trades'] > 0:
            total_profit = self.stats['avg_win'] * self.stats['winning_trades']
            total_loss = abs(self.stats['avg_loss'] * self.stats['losing_trades'])
            self.stats['profit_factor'] = total_profit / total_loss if total_loss > 0 else 0
            
        if total_trades > 0:
            win_prob = self.stats['win_rate'] / 100
            self.stats['expectancy'] = (win_prob * self.stats['avg_win']) + ((1 - win_prob) * self.stats['avg_loss'])
            
        current_balance = self.virtual_balance if self.virtual_mode else self.get_real_balance()
        if current_balance > self.stats['peak_balance']:
            self.stats['peak_balance'] = current_balance
            self.stats['current_drawdown'] = 0
        else:
            self.stats['current_drawdown'] = ((self.stats['peak_balance'] - current_balance) / self.stats['peak_balance']) * 100
            self.stats['max_drawdown'] = max(self.stats['max_drawdown'], self.stats['current_drawdown'])

        if current_balance > self.stats['session_high']:
            self.stats['session_high'] = current_balance
        if current_balance < self.stats['session_low']:
            self.stats['session_low'] = current_balance

        # Обновление данных для машинного обучения
        if self.use_ml:
            features = [
                self.market_conditions.get('trend_strength', 0),
                self.market_conditions.get('rsi', 50),
                self.market_conditions.get('volatility', 0),
            ]
            if self.indicator_settings.get('use_macd', False):
                features.append(self.market_conditions.get('macd_hist', 0))
            result_flag = 1 if trade_result.net_pnl > 0 else 0
            self.ml_agent.add_record(features, result_flag)
            self.ml_agent.train()

    def send_enhanced_trade_notification(self, action, trade_result=None, reason=""):
        """Улучшенное уведомление о сделке"""
        mode = "🎮 ВИРТУАЛЬНАЯ" if self.virtual_mode else "💰 РЕАЛЬНАЯ"
        
        if action == 'open':
            pos = self.current_position
            stops_info = pos.get('stops_info', {})
            
            message = f"""
🚀 <b>{mode} СДЕЛКА ОТКРЫТА</b>

📊 <b>Сигнал:</b> {pos['side'].upper()} ({pos['signal_reason']})
💪 <b>Сила:</b> {pos['signal_strength']:.2f}
💰 <b>Размер:</b> {pos['quantity']:.6f} @ ${pos['entry_price']:.6f}

🎯 <b>Стопы (ATR-based):</b>
🟢 TP: ${pos['take_profit']:.6f} (+{stops_info.get('tp_percent', 0):.1f}%)
🔴 SL: ${pos['stop_loss']:.6f} (-{stops_info.get('stop_percent', 0):.1f}%)
⚖️ R:R = 1:{stops_info.get('risk_reward', 1.5):.1f}

💪 <b>Мартингейл:</b> Уровень {self.martingale_index + 1}/6 ({self.napalm_fractions[self.martingale_index]*100:.0f}%)
📈 <b>Тренд:</b> {self.market_conditions['trend_direction']} ({self.market_conditions['trend_strength']:.0f}%)
            """
            
        else:
            result = trade_result
            profit_emoji = "🟢" if result.net_pnl > 0 else "🔴"
            
            message = f"""
{profit_emoji} <b>{mode} СДЕЛКА ЗАКРЫТА</b>

📊 <b>Причина:</b> {reason}
💰 <b>PnL:</b> ${result.net_pnl:.2f} ({result.pnl_percent:+.2f}%)

📈 <b>Детали:</b>
• Сигнал: {result.signal_reason}
• Сила: {result.signal_strength:.2f}
• Время: {str(result.hold_time).split('.')[0]}

💼 <b>Баланс:</b> ${self.virtual_balance if self.virtual_mode else self.get_real_balance():.2f}
🎯 <b>Винрейт:</b> {self.stats['win_rate']:.1f}% ({self.stats['winning_trades']}/{self.stats['total_trades']})
            """
            
        self.send_telegram_message(message)

    def get_current_price(self):
        """Получение текущей цены"""
        try:
            ticker = self.exchange.fetch_ticker(self.current_symbol)
            return ticker['last']
        except Exception as e:
            logging.error(f"Ошибка получения цены: {e}")
            return None

    def get_real_balance(self):
        """Получение реального баланса"""
        try:
            balance = self.exchange.fetch_balance()
            return balance['USDT']['free']
        except:
            return START_BALANCE

    def send_napalm_performance_report(self):
        """НАПАЛМОВЫЙ отчет производительности"""
        balance = self.virtual_balance if self.virtual_mode else self.get_real_balance()
        total_return = ((balance / START_BALANCE) - 1) * 100
        
        uptime = datetime.now() - self.stats['start_time']
        hours = uptime.total_seconds() / 3600
        hourly_return = total_return / hours if hours > 0 else 0
        target_progress = (total_return / 344) * 100
        
        mode = "🎮 ВИРТУАЛЬНЫЙ" if self.virtual_mode else "💰 РЕАЛЬНЫЙ"
        
        message = f"""
🔥🔥🔥 <b>НАПАЛМ PRO V2 ОТЧЕТ</b> 🔥🔥🔥

💰 <b>ФИНАНСЫ ({mode}):</b>
• Баланс: ${balance:.2f}
• Прибыль: ${balance - START_BALANCE:.2f}
• ROI: {total_return:+.1f}%
• В час: {hourly_return:+.2f}%/ч
• Прогресс к 344%: {target_progress:.1f}%

📊 <b>УЛУЧШЕННАЯ СТАТИСТИКА:</b>
• Всего сделок: {self.stats['total_trades']}
• Винрейт: {self.stats['win_rate']:.1f}% ({self.stats['winning_trades']}/{self.stats['total_trades']})
• Profit Factor: {self.stats['profit_factor']:.2f}
• Expectancy: ${self.stats['expectancy']:.2f}

🎯 <b>НОВЫЕ СИГНАЛЫ V2:</b>
• Pullback входы: {self.stats['pullback_entries']}
• Momentum входы: {self.stats['momentum_entries']}
• Блокировок трендом: {self.stats['trend_blocks']}
• Усилений трендом: {self.stats['trend_enhancements']}
• Ложных блокировок: {self.stats['false_signals_blocked']}

🎯 <b>ТЕКУЩЕЕ СОСТОЯНИЕ:</b>
• Мартингейл: {self.martingale_index + 1}/6 ({self.napalm_fractions[self.martingale_index]*100:.0f}%)
• Тренд: {self.market_conditions['trend_direction']} ({self.market_conditions['trend_strength']:.0f}%)
• RSI: {self.market_conditions['rsi']:.1f}

⏰ <b>Время работы:</b> {str(uptime).split('.')[0]}
        """
        
        self.send_telegram_message(message)

    # Все остальные методы команд
    def send_trend_status(self):
        """Статус трендового фильтра"""
        status = "✅ ВКЛЮЧЕН" if self.trend_filter.enabled else "❌ ВЫКЛЮЧЕН"
        mode = CURRENT_TREND_MODE.upper()
        
        message = f"""
🎯 <b>ТРЕНДОВЫЙ ФИЛЬТР V2</b>

📊 <b>Статус:</b> {status}
🎚 <b>Режим:</b> {mode}
📈 <b>EMA период:</b> {self.trend_filter.ema_period}

📈 <b>Текущий рынок:</b>
• Направление: {self.market_conditions['trend_direction']}
• Сила: {self.market_conditions['trend_strength']:.0f}%

📊 <b>Статистика фильтра:</b>
• Заблокировано: {self.stats['trend_blocks']}
• Усилено: {self.stats['trend_enhancements']}
• Ложных блокировок: {self.stats['false_signals_blocked']}
        """
        
        self.send_telegram_message(message)

    def cycle_trend_mode(self):
        """Переключение режима трендового фильтра"""
        global CURRENT_TREND_MODE
        modes = ['conservative', 'moderate', 'aggressive']
        current_index = modes.index(CURRENT_TREND_MODE)
        new_index = (current_index + 1) % len(modes)
        new_mode = modes[new_index]
        CURRENT_TREND_MODE = new_mode
        
        new_settings = TREND_MODES[new_mode]
        self.trend_filter.block_against_trend = new_settings['block_against_trend']
        self.trend_filter.enhance_with_trend = new_settings['enhance_with_trend']
        self.trend_filter.neutral_zone_trading = new_settings['neutral_zone_trading']
        self.trend_filter.min_trend_confidence = new_settings['min_trend_confidence']
        
        mode_emoji = {'conservative': '🛡️', 'moderate': '⚖️', 'aggressive': '⚡'}
        
        message = f"""
{mode_emoji[new_mode]} <b>РЕЖИМ ТРЕНДА: {new_mode.upper()}</b>

📊 <b>Настройки:</b>
• Блокировка против тренда: {"✅" if new_settings['block_against_trend'] else "❌"}
• Усиление по тренду: {"✅" if new_settings['enhance_with_trend'] else "❌"}
• Мин. уверенность: {new_settings['min_trend_confidence']}%
        """
        
        self.send_telegram_message(message)

    def disable_trend_filter(self):
        """Отключение трендового фильтра"""
        self.trend_filter.enabled = False
        self.send_telegram_message("❌ <b>ТРЕНДОВЫЙ ФИЛЬТР ОТКЛЮЧЕН</b>\n\n⚠️ Все сигналы будут проходить")

    def enable_trend_filter(self):
        """Включение трендового фильтра"""
        self.trend_filter.enabled = True
        self.send_telegram_message("✅ <b>ТРЕНДОВЫЙ ФИЛЬТР ВКЛЮЧЕН</b>\n\n🎯 Защита от ложных сигналов активна")

    def send_enhanced_status(self):
        """Улучшенный статус бота"""
        uptime = datetime.now() - self.stats['start_time']
        uptime_str = str(uptime).split('.')[0]
        
        mode = "🎮 ВИРТУАЛЬНЫЙ" if self.virtual_mode else "💰 РЕАЛЬНЫЙ"
        balance = self.virtual_balance if self.virtual_mode else self.get_real_balance()
        roi = ((balance / START_BALANCE - 1) * 100)
        
        message = f"""
🤖 <b>NAPALM PRO V2 STATUS</b>

🔥 <b>Состояние:</b> 🟢 РАБОТАЕТ
🎯 <b>Режим:</b> {mode}
⏰ <b>Время работы:</b> {uptime_str}
💰 <b>Баланс:</b> ${balance:.2f} ({roi:+.1f}%)

📊 <b>Улучшения V2:</b>
• Pullback Entry стратегия: ✅
• Трендовый фильтр: {"✅" if self.trend_filter.enabled else "❌"}
• Динамические ATR стопы: ✅

💪 <b>Текущее состояние:</b>
• Мартингейл: {self.martingale_index + 1}/6 ({self.napalm_fractions[self.martingale_index]*100:.0f}%)
• Тренд: {self.market_conditions['trend_direction']} ({self.market_conditions['trend_strength']:.0f}%)
• RSI: {self.market_conditions['rsi']:.1f}
        """
        
        self.send_telegram_message(message)

    def send_enhanced_help(self):
        """Расширенная справка V2"""
        message = """
🆘 <b>NAPALM PRO V2 КОМАНДЫ</b>

🎯 <b>НОВОЕ: Трендовый фильтр</b>
/trend - Статус трендового фильтра
/trend_mode - Переключить режим
/trend_on - Включить фильтр
/trend_off - Отключить фильтр

📈 <b>Информация:</b>
/napalm - НАПАЛМОВАЯ статистика V2
/stats - Альтернатива /napalm
/position - Текущая позиция
/balance - Баланс
/status - Статус бота V2

🎮 <b>Режимы:</b>
/virtual - Виртуальная торговля
/real - Реальная торговля
/aggressive - Агрессивный режим
/turbo - Турбо режим

🛑 <b>Управление:</b>
/stop - Остановить бота
/reset - Сброс мартингейла

🔥 <b>УЛУЧШЕНИЯ V2:</b>
✅ Pullback Entry (вместо Late Entry)
✅ Исправленный трейлинг стоп
✅ Трендовый фильтр с EMA
✅ RSI и Bollinger Bands фильтры
✅ Динамические ATR стопы
        """
        self.send_telegram_message(message)

    def handle_stop_command(self):
        """Остановка бота с финальным отчетом"""
        self.should_stop = True
        self.is_running = False
        
        mode = "🎮 ВИРТУАЛЬНЫЙ" if self.virtual_mode else "💰 РЕАЛЬНЫЙ"
        balance = self.virtual_balance if self.virtual_mode else self.get_real_balance()
        profit = balance - START_BALANCE
        roi = (profit / START_BALANCE) * 100
        
        message = f"""
⛔ <b>NAPALM PRO V2 ОСТАНОВЛЕН</b>

🎯 <b>ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:</b>
• Режим: {mode}
• Баланс: ${balance:.2f}
• Прибыль: ${profit:.2f} ({roi:+.1f}%)
• Сделок: {self.stats['total_trades']}
• Винрейт: {self.stats['win_rate']:.1f}%

🎯 <b>УЛУЧШЕНИЯ V2:</b>
• Pullback входов: {self.stats['pullback_entries']}
• Momentum входов: {self.stats['momentum_entries']}
• Трендовых блокировок: {self.stats['trend_blocks']}
• Трендовых усилений: {self.stats['trend_enhancements']}

🔥 Спасибо за использование NAPALM PRO V2!
        """
        
        self.send_telegram_message(message)
        logging.info("⛔ NAPALM PRO V2 остановлен")

    def handle_reset_command(self):
        """Сброс мартингейла"""
        old_level = self.martingale_index
        self.martingale_index = 0
        self.consecutive_losses = 0
        self.recovery_mode = False
        
        message = f"""
🔄 <b>СБРОС МАРТИНГЕЙЛА V2</b>

📊 <b>Было:</b> Уровень {old_level + 1}/6 ({self.napalm_fractions[old_level]*100:.0f}%)
✅ <b>Стало:</b> Уровень 1/6 ({self.napalm_fractions[0]*100:.0f}%)
🔥 <b>Серия убытков сброшена!</b>
        """
        
        self.send_telegram_message(message)

    def toggle_turbo_mode(self):
        """Переключение турбо режима"""
        self.turbo_mode = not self.turbo_mode
        self.feature_flags['turbo_mode'] = self.turbo_mode
        
        if self.turbo_mode:
            message = "⚡ <b>TURBO РЕЖИМ V2 ВКЛЮЧЕН!</b>\n\n🔥 +50% к размерам позиций"
        else:
            message = "❄️ <b>TURBO РЕЖИМ ВЫКЛЮЧЕН</b>\n\n✅ Стандартные размеры"
        
        self.send_telegram_message(message)

    def toggle_aggressive_mode(self):
        """Переключение агрессивного режима"""
        if self.aggressive_multiplier == 1.0:
            self.aggressive_multiplier = 2.0
            message = "🔥 <b>АГРЕССИВНЫЙ РЕЖИМ V2 ВКЛЮЧЕН!</b>\n\n⚡ Размеры позиций увеличены в 2 раза!"
            self.feature_flags['aggressive_mode'] = True
        else:
            self.aggressive_multiplier = 1.0
            message = "❄️ <b>АГРЕССИВНЫЙ РЕЖИМ ВЫКЛЮЧЕН</b>\n\n✅ Стандартные размеры позиций"
            self.feature_flags['aggressive_mode'] = False
        
        self.send_telegram_message(message)

    def toggle_trailing_stop(self):
        """Переключение улучшенного трейлинг стопа"""
        self.trailing_stop_enabled = not self.trailing_stop_enabled
        self.feature_flags['trailing_stop'] = self.trailing_stop_enabled
        
        if self.trailing_stop_enabled:
            message = f"🔵 <b>TRAILING STOP V2 ВКЛЮЧЕН!</b>\n\n✅ Активация только при прибыли >{self.min_profit_for_trailing}%"
        else:
            message = "⭕ <b>TRAILING STOP ВЫКЛЮЧЕН</b>\n\n📊 Только фиксированные стопы TP/SL"
        
        self.send_telegram_message(message)

    def set_machine_learning(self, enabled: bool):
        """Включение или отключение машинного обучения"""
        self.use_ml = bool(enabled)
        self.feature_flags['machine_learning'] = self.use_ml

    def switch_to_virtual_mode(self):
        """Переключение на виртуальную торговлю"""
        if self.virtual_mode:
            self.send_telegram_message("⚠️ Уже в виртуальном режиме!")
            return
            
        if self.current_position:
            self.send_telegram_message("⚠️ Закройте реальную позицию!")
            return
            
        self.virtual_mode = True
        self.send_telegram_message("🎮 <b>Переключено на ВИРТУАЛЬНЫЙ режим V2</b>")

    def switch_to_real_mode(self):
        """Переключение на реальную торговлю"""
        if not self.virtual_mode:
            self.send_telegram_message("⚠️ Уже в реальном режиме!")
            return
            
        if self.current_position:
            self.send_telegram_message("⚠️ Закройте виртуальную позицию!")
            return
            
        balance = self.virtual_balance
        profit = balance - START_BALANCE
        roi = (profit / START_BALANCE) * 100
        
        message = f"""
💰 <b>ПЕРЕКЛЮЧЕНИЕ НА РЕАЛЬНУЮ ТОРГОВЛЮ V2?</b>

📊 <b>Виртуальные результаты:</b>
• Баланс: ${balance:.2f}
• Прибыль: ${profit:.2f} ({roi:+.1f}%)
• Винрейт: {self.stats['win_rate']:.1f}%
• Pullback входов: {self.stats['pullback_entries']}

⚠️ <b>ВНИМАНИЕ!</b> Реальные деньги!
        """
        
        self.send_telegram_message(message)

    def send_balance(self):
        """Отправка баланса"""
        try:
            if self.virtual_mode:
                balance = self.virtual_balance
                mode = "🎮 ВИРТУАЛЬНЫЙ"
            else:
                balance = self.get_real_balance()
                mode = "💰 РЕАЛЬНЫЙ"
                
            profit = balance - START_BALANCE
            roi = (profit / START_BALANCE * 100) if START_BALANCE > 0 else 0
            
            message = f"""
💰 <b>БАЛАНС NAPALM V2 - {mode}</b>

💵 <b>Текущий:</b> ${balance:.2f}
🏦 <b>Стартовый:</b> ${START_BALANCE:.2f}
📈 <b>Прибыль:</b> ${profit:.2f}
📊 <b>ROI:</b> {roi:+.1f}%

{'🟢 ОТЛИЧНО!' if roi > 50 else '🟡 ХОРОШО!' if roi > 10 else '💪 НЕ СДАЕМСЯ!'}
            """
            
            self.send_telegram_message(message)
            
        except Exception as e:
            self.send_telegram_message(f"❌ Ошибка баланса: {e}")

    def send_position_info(self):
        """Информация о текущей позиции"""
        if not self.current_position:
            self.send_telegram_message("📊 Нет открытых позиций")
            return
            
        pos = self.current_position
        current_price = self.get_current_price()
        if not current_price:
            return
            
        if pos['side'] == 'buy':
            pnl = (current_price - pos['entry_price']) * pos['quantity']
        else:
            pnl = (pos['entry_price'] - current_price) * pos['quantity']
            
        pnl_percent = (pnl / (pos['entry_price'] * pos['quantity'])) * 100
        hold_time = datetime.now() - pos['time']
        
        mode = "🎮 ВИРТУАЛЬНАЯ" if pos.get('virtual', False) else "💰 РЕАЛЬНАЯ"
        profit_emoji = "🟢" if pnl > 0 else "🔴"
        
        message = f"""
📊 <b>ТЕКУЩАЯ ПОЗИЦИЯ V2</b>

{mode}
🎯 <b>Сигнал:</b> {pos['side'].upper()} ({pos.get('signal_reason', 'Unknown')})
💰 <b>Размер:</b> {pos['quantity']:.6f}
💵 <b>Вход:</b> ${pos['entry_price']:.6f}
📈 <b>Текущая:</b> ${current_price:.6f}

{profit_emoji} <b>PnL:</b> ${pnl:.2f} ({pnl_percent:+.2f}%)

⏱ <b>Время:</b> {str(hold_time).split('.')[0]}
        """
        
        self.send_telegram_message(message)

    def send_last_trades_report(self):
        """Отчет по последним сделкам"""
        if not self.position_history:
            self.send_telegram_message("📊 История сделок пуста")
            return
            
        last_trades = self.position_history[-10:]
        
        message = "📊 <b>ПОСЛЕДНИЕ СДЕЛКИ V2:</b>\n\n"
        
        for i, trade in enumerate(reversed(last_trades), 1):
            result = trade['result']
            emoji = "🟢" if result.net_pnl > 0 else "🔴"
            reason_short = result.signal_reason.split()[0] if hasattr(result, 'signal_reason') else "Unknown"
            
            message += f"{i}. {emoji} {result.side.upper()} "
            message += f"${result.net_pnl:.2f} ({result.pnl_percent:+.1f}%) "
            message += f"- {reason_short}\n"
            
        total_pnl = sum(t['result'].net_pnl for t in last_trades)
        wins = sum(1 for t in last_trades if t['result'].net_pnl > 0)
        
        message += f"\n<b>Итого:</b> ${total_pnl:.2f} | Побед: {wins}/{len(last_trades)}"
        
        self.send_telegram_message(message)

    def set_brick_size(self, command):
        """Установка размера кирпича"""
        try:
            parts = command.split()
            if len(parts) > 1:
                new_size = float(parts[1])
                if 0.0001 <= new_size <= 10:
                    old_size = self.adaptive_brick_size
                    self.adaptive_brick_size = new_size
                    self.send_telegram_message(f"🧱 Размер кирпича V2: ${old_size:.6f} → ${new_size:.6f}")
                else:
                    self.send_telegram_message("❌ Размер должен быть от $0.0001 до $10")
            else:
                self.send_telegram_message(f"🧱 Текущий размер: ${self.adaptive_brick_size:.6f}")
        except:
            self.send_telegram_message("❌ Ошибка. Используйте: /brick 0.005")

    def set_take_profit(self, command):
        """Установка тейк профита"""
        try:
            parts = command.split()
            if len(parts) > 1:
                new_tp = float(parts[1])
                if 0.5 <= new_tp <= 20:
                    self.send_telegram_message(f"🟢 TP V2: {new_tp}% (динамические ATR стопы)")
                else:
                    self.send_telegram_message("❌ TP должен быть от 0.5% до 20%")
            else:
                self.send_telegram_message("🟢 TP рассчитывается динамически на основе ATR")
        except:
            self.send_telegram_message("❌ Ошибка. Используйте: /tp 4")

    def set_stop_loss(self, command):
        """Установка стоп лосса"""
        try:
            parts = command.split()
            if len(parts) > 1:
                new_sl = float(parts[1])
                if 0.5 <= new_sl <= 20:
                    self.send_telegram_message(f"🔴 SL V2: {new_sl}% (динамические ATR стопы)")
                else:
                    self.send_telegram_message("❌ SL должен быть от 0.5% до 20%")
            else:
                self.send_telegram_message("🔴 SL рассчитывается динамически на основе ATR")
        except:
            self.send_telegram_message("❌ Ошибка. Используйте: /sl 3")

    def run_enhanced_trading_loop(self):
        """Улучшенный основной торговый цикл V2"""
        logging.info("🚀 Запуск улучшенного торгового цикла V2")
        
        iteration_count = 0
        last_stats_time = time.time()
        
        while self.is_running and not self.should_stop:
            try:
                iteration_count += 1
                
                if self.current_position:
                    self.check_enhanced_position_stops()
                
                df = self.get_renko_data()
                if df is None:
                    time.sleep(15)
                    continue
                
                df = self.calculate_technical_indicators(df)
                bricks = self.build_smart_renko_v2(df)
                
                if self.has_new_brick(bricks):
                    logging.info(f"🧱 Новый кирпич! Всего: {len(bricks)}")
                    
                    can_trade = not bool(self.current_position)
                    
                    if can_trade:
                        signal, strength, reason = self.analyze_revolutionary_signals(bricks, df)
                        
                        if signal and strength >= 0.4:
                            logging.info(f"🎯 СИГНАЛ V2: {signal.upper()} (сила: {strength:.2f}) - {reason}")
                            
                            quantity = self.calculate_enhanced_position_size(strength, reason)
                            
                            if quantity > 0:
                                success = self.execute_trade_with_enhanced_stops(signal, quantity, strength, reason)
                                
                                if success:
                                    logging.info("✅ Сделка V2 открыта!")
                                    
                                    if "Pullback" in reason:
                                        motivational = random.choice([
                                            "🎯 ОТЛИЧНЫЙ ВХОД НА ОТКАТЕ!",
                                            "🚀 PULLBACK СТРАТЕГИЯ РАБОТАЕТ!",
                                            "💥 ПОЙМАЛИ РАЗВОРОТ!"
                                        ])
                                    else:
                                        motivational = random.choice([
                                            "⚡ MOMENTUM CAPTURED!",
                                            "🔥 НАПАЛМ V2 В ДЕЙСТВИИ!",
                                            "💪 СИГНАЛ ИСПОЛНЕН!"
                                        ])
                                    
                                    self.send_telegram_message(motivational)
                                else:
                                    logging.error("❌ Не удалось открыть сделку V2")
                        else:
                            if signal:
                                logging.info(f"⚠️ Слабый сигнал: {signal} (сила: {strength:.2f}) - {reason}")
                            else:
                                logging.info(f"ℹ️ Нет сигнала: {reason}")
                
                if time.time() - last_stats_time > 1800:
                    self.send_napalm_performance_report()
                    last_stats_time = time.time()
                
                if self.virtual_mode:
                    current_balance = self.virtual_balance
                else:
                    current_balance = self.get_real_balance()
                
                if current_balance > self.stats['session_high']:
                    self.stats['session_high'] = current_balance
                if current_balance < self.stats['session_low']:
                    self.stats['session_low'] = current_balance
                
                time.sleep(10)
                
            except KeyboardInterrupt:
                logging.info("⛔ Остановка по Ctrl+C")
                break
            except Exception as e:
                logging.error(f"💥 Ошибка в цикле V2: {e}")
                time.sleep(30)
        
        if self.should_stop:
            self.send_telegram_message("✅ <b>NAPALM PRO V2 ОСТАНОВЛЕН</b>\n\n🔥 Работа завершена успешно!")
            self.send_napalm_performance_report()

        logging.info("🏁 Улучшенный торговый цикл V2 завершен")

    def run(self):
        """Entry point used by external controllers."""
        self.run_enhanced_trading_loop()

# Запуск улучшенного бота
if __name__ == "__main__":
    try:
        print("🔥🔥🔥 NAPALM PRO BOT V2 - РЕВОЛЮЦИОННЫЕ УЛУЧШЕНИЯ 🔥🔥🔥")
        print("=" * 60)
        print("КЛЮЧЕВЫЕ ИСПРАВЛЕНИЯ:")
        print("✅ Pullback Entry стратегия (исправлен Late Entry)")
        print("✅ Исправленный трейлинг стоп (только при прибыли)")
        print("✅ Трендовый фильтр с EMA")
        print("✅ RSI и Bollinger Bands фильтры")
        print("✅ Динамические ATR стопы")
        print("✅ Улучшенная статистика и уведомления")
        print("=" * 60)
        print("Выберите режим запуска:")
        print("1. 🎮 Виртуальная торговля (РЕКОМЕНДУЕТСЯ для тестирования V2)")
        print("2. 💰 Реальная торговля (только после успешного тестирования!)")
        print()
        
        choice = input("Ваш выбор (1-2): ").strip()
        
        virtual = True
        if choice == "2":
            print("\n⚠️  ВНИМАНИЕ: Реальная торговля с V2!")
            print("Убедитесь, что виртуальное тестирование прошло успешно!")
            confirm = input("Вы протестировали V2 и готовы к реальной торговле? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                virtual = False
                print("\n💰 Выбран РЕАЛЬНЫЙ режим торговли V2")
            else:
                print("\n✅ Правильное решение! Запуск в виртуальном режиме V2")
        else:
            print("\n✅ Выбран безопасный ВИРТУАЛЬНЫЙ режим V2")
        
        print("\n🚀 Инициализация NAPALM PRO V2...")
        bot = NapalmProBotV2(virtual_mode=virtual)
        
        print("✅ NAPALM PRO V2 запущен!")
        print("\n💡 НОВЫЕ ВОЗМОЖНОСТИ V2:")
        print("• /napalm - улучшенная статистика")
        print("• /trend - трендовый фильтр")
        print("• /trend_mode - переключение режимов тренда")
        print("• Pullback Entry стратегия активна")
        print("• Исправленный трейлинг стоп")
        print("• Динамические ATR стопы")
        print("\n🔥 ПРОТЕСТИРУЙТЕ ВСЕ УЛУЧШЕНИЯ В ВИРТУАЛЬНОМ РЕЖИМЕ!")
        
        # Запуск улучшенного торгового цикла
        bot.run_enhanced_trading_loop()
        
    except KeyboardInterrupt:
        print("\n⛔ Остановка по запросу")
    except Exception as e:
        print(f"\n❌ Критическая ошибка V2: {e}")
        print("\n🔧 Проверьте:")
        print("1. API ключи в config_fixed.py")
        print("2. TELEGRAM_TOKEN и CHAT_ID")
        print("3. Подключение к интернету")
        print("4. Баланс на бирже")
        print("5. Совместимость настроек V2")
    finally:
        print("\n🏁 NAPALM PRO V2 завершен")

# Конец файла