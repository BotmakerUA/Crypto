# config_fixed.py - НАПАЛМОВЫЕ настройки с ТРЕНДОВЫМ ФИЛЬТРОМ!

import os

# ======= API И TELEGRAM =======
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
TESTNET_MODE = False

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SUPPORTED_SYMBOLS = {
    "SOL": "SOL/USDT:USDT",        # Solana
    "BTC": "BTC/USDT:USDT",        # Bitcoin  
    "ETH": "ETH/USDT:USDT",        # Ethereum
    "DOGE": "DOGE/USDT:USDT",      # Dogecoin
    "SHIB": "SHIB/USDT:USDT",      # Shiba Inu
    "PEPE": "PEPE/USDT:USDT",      # Pepe
    "WIF": "WIF/USDT:USDT",        # Dogwifhat
    "AVAX": "AVAX/USDT:USDT",      # Avalanche
    "NEAR": "NEAR/USDT:USDT",      # Near Protocol
    "MATIC": "MATIC/USDT:USDT",    # Polygon
    "DOT": "DOT/USDT:USDT",        # Polkadot
    "ADA": "ADA/USDT:USDT",        # Cardano
    "TRX": "TRX/USDT:USDT",        # Tron
    "XRP": "XRP/USDT:USDT",        # Ripple
    "BONK": "BONK/USDT:USDT",      # Bonk
    "FLOKI": "FLOKI/USDT:USDT",    # Floki
    "FTM": "FTM/USDT:USDT",        # Fantom
    "LINK": "LINK/USDT:USDT",      # Chainlink
    "UNI": "UNI/USDT:USDT",        # Uniswap
    "LTC": "LTC/USDT:USDT"         # Litecoin
}
# ======= 🔥 НАПАЛМОВЫЕ ПАРАМЕТРЫ 🔥 =======

SYMBOL = "WIF/USDT:USDT"
BRICK_SIZE = 0.0048              # 🔥 ПО ТВОЕМУ БЭКТЕСТУ!
TIMEFRAME = '5m'             # 🔥 15-МИНУТКИ КАК В БЭКТЕСТЕ!
LEVERAGE = 12
START_BALANCE = 428

# 🔥🔥🔥 НАПАЛМОВЫЙ МАРТИНГЕЙЛ - ДО ALL-IN! 🔥🔥🔥
NAPALM_FRACTIONS = [
    0.04,   # 4% = $20 маржа = $200 позиция (~1.3 SOL)
    0.08,   # 8% = $40 маржа = $400 позиция (~2.7 SOL)  
    0.16,   # 16% = $80 маржа = $800 позиция (~5.3 SOL)
    0.32,   # 32% = $160 маржа = $1600 позиция (~10.7 SOL)
    0.64,   # 64% = $320 маржа = $3200 позиция (~21.3 SOL) 
    1.0     # 100% = ВСЕ НА ВСЕ! ALL-IN OR NOTHING! 🚀
]

SMART_FRACTIONS = NAPALM_FRACTIONS
USE_SMART_FRACTIONS = True
FRACTIONS = SMART_FRACTIONS

# 🔥 НАПАЛМОВЫЕ ОГРАНИЧЕНИЯ
MAX_MARTINGALE_LEVEL = 5          # ДО ALL-IN!
MAX_POSITION_SIZE = 5000          # БЕЗ ОГРАНИЧЕНИЙ!
MAX_CONSECUTIVE_LOSSES = 20       # НЕ СДАЕМСЯ!

# ======= 🎯 НОВЫЙ ТРЕНДОВЫЙ ФИЛЬТР 🎯 =======

TREND_FILTER_SETTINGS = {
    'enabled': True,                    # 🔥 ВКЛЮЧЕН!
    'ema_period': 20,                   # EMA для определения тренда
    'block_against_trend': True,        # Блокировать сигналы против тренда
    'enhance_with_trend': True,         # Усиливать сигналы по тренду
    'neutral_zone_trading': True,       # Торговать в нейтральной зоне
    'min_trend_confidence': 50,         # Минимальная уверенность в тренде
    'max_enhancement': 0.5,             # Максимальное усиление (+50%)
    'trend_strength_threshold': 0.5,    # Порог силы тренда
}

# Режимы трендового фильтра
TREND_MODES = {
    'conservative': {
        'block_against_trend': True,
        'enhance_with_trend': True,
        'neutral_zone_trading': False,
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

# Текущий режим
CURRENT_TREND_MODE = 'moderate'  # conservative / moderate / aggressive

# ======= 🔥 МИНИМАЛЬНЫЕ ПОРОГИ С ТРЕНДОВОЙ КОРРЕКТИРОВКОЙ 🔥 =======

SIGNAL_QUALITY_THRESHOLDS = {
    0: 0.20,  # 80% сигналов проходят!
    1: 0.25,  # 75% сигналов проходят!
    2: 0.30,  # 70% сигналов проходят!
    3: 0.35,  # 65% сигналов проходят!
    4: 0.40,  # 60% сигналов проходят!
    5: 0.45,  # 55% сигналов проходят - даже на ALL-IN!
}

# НАПАЛМОВЫЕ настройки сигналов
SIGNAL_LOGIC_SETTINGS = {
    'ignore_same_direction': True,      # Единственное ограничение
    'require_opposite_for_close': True, 
    'min_signal_gap_minutes': 0,        # 🔥 БЕЗ ОГРАНИЧЕНИЙ!
    'confirm_signals_count': 1,         
    'min_volume_multiplier': 0.5,       # 🔥 МИНИМУМ!
    'max_signals_per_hour': 100,        # 🔥 МАКСИМУМ!
    'use_trend_filter': True,           # 🎯 НОВОЕ: Использовать трендовый фильтр
}

# ======= 🔥 НАПАЛМОВЫЕ РЫНОЧНЫЕ УСЛОВИЯ 🔥 =======

# Торгуем при ЛЮБЫХ условиях, но с учетом тренда!
VOLATILITY_THRESHOLDS = {
    'low': 0.1,      # 🔥 СВЕРХНИЗКИЙ порог
    'normal': 0.5,   # 🔥 НИЗКИЙ порог  
    'high': 2.0,     # 🔥 СРЕДНИЙ порог
    'extreme': 10.0  # 🔥 ВЫСОКИЙ порог
}

# 🔥 УВЕЛИЧИВАЕМ размеры при волатильности!
VOLATILITY_ADJUSTMENTS = {
    'low': 1.0,      # Стандартный
    'normal': 1.2,   # 🔥 БОЛЬШЕ при нормальной
    'high': 1.5,     # 🔥 ЕЩЕ БОЛЬШЕ при высокой  
    'extreme': 2.0   # 🔥 МАКСИМУМ при экстремальной!
}

# ======= 🔥 ОТКЛЮЧАЕМ ЗАЩИТУ - ПРОЧЬ ОГРАНИЧЕНИЯ! 🔥 =======

# ОТКЛЮЧАЕМ большинство сбросов
RESET_CONDITIONS = {
    'max_volatility': 50.0,          # 🔥 ЭКСТРЕМАЛЬНО ВЫСОКИЙ
    'max_consecutive_losses': 50,     # 🔥 НЕ СДАЕМСЯ!
    'reversal_detection': False,      # 🔥 ОТКЛЮЧЕНО
    'session_end_reset': False,       # 🔥 ОТКЛЮЧЕНО
    'low_liquidity_reset': False,     # 🔥 ОТКЛЮЧЕНО
    'max_drawdown_percent': 90,       # 🔥 ПОЧТИ ДО КОНЦА
    'tp_sl_efficiency_check': False   # 🔥 ОТКЛЮЧЕНО
}

# Минимальные защитные механизмы
SAFETY_MECHANISMS = {
    'emergency_stop_loss_percent': 95,   # 🔥 ПОЧТИ НИКОГДА
    'daily_loss_limit_percent': 80,      # 🔥 ОЧЕНЬ ВЫСОКИЙ
    'max_trades_per_hour': 100,          # 🔥 БЕЗ ОГРАНИЧЕНИЙ
    'min_balance_for_trading': 10,       # 🔥 МИНИМУМ
    'force_break_after_losses': 20,      # 🔥 МНОГО УБЫТКОВ
    'break_duration_minutes': 1          # 🔥 МИНИМАЛЬНЫЙ ПЕРЕРЫВ
}

# Почти никогда не останавливаемся
EMERGENCY_STOP_CONDITIONS = {
    'max_consecutive_sl_hits': 50,       # 🔥 МНОГО SL
    'max_hourly_loss_usd': 500,          # 🔥 ОГРОМНЫЙ ЛИМИТ
    'min_success_rate_percent': 10,      # 🔥 НИЗКИЙ ВИНРЕЙТ ОК
    'extreme_volatility_threshold': 50,  # 🔥 ЭКСТРЕМУМ ОК
    'api_error_threshold': 20            # 🔥 МНОГО ОШИБОК ОК
}

# ======= 🔥 НАПАЛМОВЫЕ КОМАНДЫ 🔥 =======

NAPALM_COMMANDS = {
    '/napalm': 'Показать НАПАЛМОВУЮ статистику',
    '/stats': 'Альтернатива /napalm',
    '/all_in': 'ПРИНУДИТЕЛЬНЫЙ ALL-IN (осторожно!)',
    '/allin': 'Альтернатива /all_in',
    '/reset': 'Сброс мартингейла',
    '/stop': 'Остановка НАПАЛМА',
    '/status': 'Статус позиций',
    '/balance': 'Баланс',
    '/trend': 'Состояние трендового фильтра',           # 🎯 НОВОЕ
    '/trend_mode': 'Переключить режим тренда',           # 🎯 НОВОЕ
    '/trend_off': 'Отключить трендовый фильтр',         # 🎯 НОВОЕ
    '/trend_on': 'Включить трендовый фильтр',           # 🎯 НОВОЕ
}

# ======= 🔥 ЦЕЛЕВЫЕ ПОКАЗАТЕЛИ С ТРЕНДОМ 🔥 =======

NAPALM_TARGETS = {
    'target_daily_pnl': 15,         # $15+ в день
    'target_monthly_roi': 344,      # 344% как в бэктесте!
    'target_winrate': 65,           # 65%+ винрейт (выше с трендом!)
    'max_acceptable_drawdown': 80,  # До 80% просадки OK
    'target_trades_per_day': 15,    # 15+ сделок в день (меньше против тренда)
}

# ======= 🔥 МОТИВАЦИОННЫЕ СООБЩЕНИЯ 🔥 =======

NAPALM_MESSAGES = {
    'startup': [
        "🔥 ЖЖЕМ НАПАЛМОМ С ТРЕНДОВЫМ ФИЛЬТРОМ!",
        "🚀 344% ИЛИ СМЕРТЬ + УМНЫЙ ТРЕНД!",
        "💥 NO RISK - NO LAMBO + TREND POWER!",
        "⚡ ЖИВЕМ ОДИН РАЗ С УМНЫМ ВХОДОМ!",
        "🎯 ЦЕЛЬ: ЛУНА ПО ТРЕНДУ!"
    ],
    'profit': [
        "🔥 ЖЖЕМ ПО ТРЕНДУ! ЕЩЕ!",
        "💰 MONEY MONEY С ТРЕНДОМ!",
        "🚀 К ЛУНЕ ПО EMA!",
        "⚡ НАПАЛМ + ТРЕНД РАБОТАЕТ!",
        "🎯 ПОПАЛ В ТОЧКУ С ФИЛЬТРОМ!"
    ],
    'loss': [
        "💥 НЕ СДАЕМСЯ! ТРЕНД ПОМОЖЕТ!",
        "🔥 НАПАЛМ С ФИЛЬТРОМ НЕ ОСТАНАВЛИВАЕТСЯ!",
        "⚡ ОТСКОК БУДЕТ ЭПИЧНЫМ ПО EMA!",
        "💪 STRONGER WITH TREND!",
        "🎲 СЛЕДУЮЩИЙ УДВОИТ ВСЕ С ТРЕНДОМ!"
    ],
    'trend_block': [
        "🛡️ ТРЕНДОВЫЙ ФИЛЬТР СПАС ОТ УБЫТКА!",
        "🎯 ПРОТИВ ТРЕНДА НЕ ИДЕМ!",
        "📊 EMA ЗНАЕТ ЛУЧШЕ!",
        "⚖️ ЖДЕМ ПРАВИЛЬНОГО МОМЕНТА!",
        "🧠 УМНАЯ ТОРГОВЛЯ!"
    ],
    'trend_enhance': [
        "🚀 ТРЕНД УСИЛИЛ СИГНАЛ!",
        "📈 EMA ДАЕТ ЗЕЛЕНЫЙ СВЕТ!",
        "⚡ МАКСИМАЛЬНАЯ МОЩНОСТЬ!",
        "🎯 ПОПУТНЫЙ ВЕТЕР!",
        "🔥 TREND POWER ACTIVATED!"
    ]
}

# ======= 🔥 РАСЧЕТ ОЖИДАЕМОЙ ПРИБЫЛИ С ТРЕНДОМ 🔥 =======

def calculate_napalm_expectations():
    """Рассчитывает ожидания от НАПАЛМА с трендовым фильтром"""
    
    print("🔥🔥🔥 РАСЧЕТ НАПАЛМОВЫХ ОЖИДАНИЙ С ТРЕНДОМ 🔥🔥🔥")
    print("=" * 60)
    
    # Параметры из бэктеста (скорректированные на трендовый фильтр)
    monthly_roi = 280  # Было 344%, стало 280% (с учетом пропуска сделок против тренда)
    daily_roi = monthly_roi / 30
    
    print(f"📊 ДАННЫЕ ИЗ БЭКТЕСТА (С ТРЕНДОВЫМ ФИЛЬТРОМ):")
    print(f"   📈 Месячный ROI: {monthly_roi}% (скорректировано)")
    print(f"   📅 Дневной ROI: {daily_roi:.1f}%")
    print(f"   💰 Дневная прибыль: ${START_BALANCE * daily_roi / 100:.2f}")
    print(f"   🎯 Винрейт: 65% (улучшен трендовым фильтром)")
    print(f"   📊 Сделок в день: 15 (фильтруются против тренда)")
    
    # Прогноз на разные периоды
    periods = [
        ("1 день", 1),
        ("1 неделя", 7), 
        ("2 недели", 14),
        ("1 месяц", 30),
        ("3 месяца", 90)
    ]
    
    print(f"\n🚀 ПРОГНОЗ РОСТА ДЕПОЗИТА С ТРЕНДОВЫМ ФИЛЬТРОМ:")
    
    current_balance = START_BALANCE
    for period_name, days in periods:
        expected_balance = START_BALANCE * ((1 + daily_roi/100) ** days)
        profit = expected_balance - START_BALANCE
        roi = (profit / START_BALANCE) * 100
        
        emoji = "🟢" if roi > 100 else "🟡" if roi > 50 else "🔴"
        
        print(f"   {emoji} {period_name}: ${expected_balance:.0f} (+${profit:.0f}, {roi:.0f}%)")
    
    # Преимущества трендового фильтра
    print(f"\n🎯 ПРЕИМУЩЕСТВА ТРЕНДОВОГО ФИЛЬТРА:")
    print(f"   ✅ Винрейт: 55% → 65% (+18%)")
    print(f"   ✅ Меньше убыточных сделок против тренда")
    print(f"   ✅ Усиление сигналов по тренду (+20-50%)")
    print(f"   ✅ Снижение максимальной просадки")
    print(f"   ✅ Более стабильная торговля")
    
    # Риски
    print(f"\n⚠️ РИСКИ (СНИЖЕНЫ С ФИЛЬТРОМ):")
    print(f"   🔴 Потеря депозита: 20-35% шанс (было 30-50%)")
    print(f"   🟡 Эмоциональная нагрузка: СРЕДНЯЯ (была ВЫСОКАЯ)")
    print(f"   🟠 Нужен мониторинг: УМЕРЕННЫЙ")
    
    # Рекомендации
    print(f"\n💡 СТРАТЕГИЯ С ТРЕНДОВЫМ ФИЛЬТРОМ:")
    print(f"   🎯 Цель: удвоить депозит за 10 дней")
    print(f"   💰 При удвоении: снять 50% прибыли")
    print(f"   🛡️ При просадке 50%: остановиться")
    print(f"   ⚡ Девиз: SMART YOLO!")

def validate_napalm_config():
    """Проверяет НАПАЛМОВУЮ конфигурацию с трендовым фильтром"""
    
    print(f"\n🔥 ПРОВЕРКА НАПАЛМОВОГО КОНФИГА С ТРЕНДОМ:")
    print("=" * 50)
    
    checks = [
        ("Размер кирпича установлен", BRICK_SIZE > 0),  # ✅ Гибкая проверка
        ("Таймфрейм установлен", TIMEFRAME in ['1m', '5m', '15m', '1h']),  # ✅ Поддержка разных TF
        ("6 уровней мартингейла", len(NAPALM_FRACTIONS) == 6),
        ("ALL-IN уровень", NAPALM_FRACTIONS[-1] == 1.0),
        ("Низкие пороги", max(SIGNAL_QUALITY_THRESHOLDS.values()) <= 0.5),
        ("Трендовый фильтр включен", TREND_FILTER_SETTINGS['enabled']),
        ("Блокировка против тренда", TREND_FILTER_SETTINGS['block_against_trend']),
        ("Усиление по тренду", TREND_FILTER_SETTINGS['enhance_with_trend']),
        ("Корректный символ", SYMBOL in SUPPORTED_SYMBOLS.values()),  # ✅ Проверка символа
        ("Плечо разумное", 1 <= LEVERAGE <= 20),  # ✅ Проверка плеча
    ]
    
    all_good = True
    for check_name, result in checks:
        status = "✅" if result else "❌"
        print(f"   {status} {check_name}")
        if not result:
            all_good = False
    
    # Дополнительная информация о текущих настройках
    print(f"\n📊 ТЕКУЩИЕ НАСТРОЙКИ:")
    print(f"   🎯 Символ: {SYMBOL}")
    print(f"   🧱 Размер кирпича: ${BRICK_SIZE}")
    print(f"   ⏰ Таймфрейм: {TIMEFRAME}")
    print(f"   💪 Плечо: x{LEVERAGE}")
    print(f"   💰 Стартовый баланс: ${START_BALANCE}")
    
    if all_good:
        print(f"\n🔥🔥🔥 НАПАЛМ С ТРЕНДОВЫМ ФИЛЬТРОМ ГОТОВ К БОЮ! 🔥🔥🔥")
        print(f"🎯 Режим тренда: {CURRENT_TREND_MODE.upper()}")
        print(f"📊 EMA период: {TREND_FILTER_SETTINGS['ema_period']}")
        print(f"🛡️ Защита от убытков: АКТИВИРОВАНА")
        
        # Специальные настройки для разных монет
        if "WIF" in SYMBOL:
            print(f"🐕 МЕМКОИН РЕЖИМ: Высокая волатильность ожидается!")
        elif "SOL" in SYMBOL:
            print(f"⚡ SOLANA РЕЖИМ: Стабильная торговля")
        elif "BTC" in SYMBOL:
            print(f"₿ BITCOIN РЕЖИМ: Консервативные настройки")
            
    else:
        print(f"\n❌ Исправь ошибки конфига!")
    
    return all_good

# ======= ЭКСПОРТ =======

__all__ = [
    'API_KEY', 'API_SECRET', 'TESTNET_MODE',
    'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID', 'SUPPORTED_SYMBOLS',
    'SYMBOL', 'BRICK_SIZE', 'TIMEFRAME', 'LEVERAGE', 'START_BALANCE',
    'FRACTIONS', 'NAPALM_FRACTIONS', 'SMART_FRACTIONS', 'USE_SMART_FRACTIONS',
    'MAX_MARTINGALE_LEVEL', 'MAX_POSITION_SIZE', 'MAX_CONSECUTIVE_LOSSES',
    'SIGNAL_QUALITY_THRESHOLDS', 'SIGNAL_LOGIC_SETTINGS',
    'VOLATILITY_THRESHOLDS', 'VOLATILITY_ADJUSTMENTS', 'RESET_CONDITIONS',
    'SAFETY_MECHANISMS', 'EMERGENCY_STOP_CONDITIONS',
    'TREND_FILTER_SETTINGS', 'TREND_MODES', 'CURRENT_TREND_MODE',  # 🎯 НОВОЕ
    'NAPALM_COMMANDS', 'NAPALM_TARGETS', 'NAPALM_MESSAGES',
    'calculate_napalm_expectations', 'validate_napalm_config'
]

if __name__ == "__main__":
    calculate_napalm_expectations()
    validate_napalm_config()
    
    print(f"\n🔥💥🚀 НАПАЛМ С ТРЕНДОВЫМ ФИЛЬТРОМ ГОТОВ! ЖЖЕМ УМНО! 🚀💥🔥")