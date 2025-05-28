import ccxt
import pandas as pd
import numpy as np
import requests
import logging
from datetime import datetime
import pytz
import talib

# Configuration
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1377383087209451703/xnoJnt4PnHnZEiU2FLlYojnEdTnQqpZlK-F6oi7NiY1DAhGf8NGb21Ko_uBVqxOXbmN1'
SYMBOLS = ['BTC-USDT-SWAP', 'ETH-USDT-SWAP', 'BTC-USD-SWAP', 'SOL-USDT-SWAP', 'ETH-USD-SWAP', 'DOGE-USDT-SWAP', 'XRP-USDT-SWAP', 'SUI-USDT-SWAP', 'PEPE-USDT-SWAP', 'LTC-USDT-SWAP', 'TRUMP-USDT-SWAP', 'DOGE-USD-SWAP', 'ADA-USDT-SWAP', 'SOL-USD-SWAP', 'BTC-USDC-SWAP', 'BNB-USDT-SWAP', 'AVAX-USDT-SWAP', 'AAVE-USDT-SWAP', 'BCH-USDT-SWAP', 'TON-USDT-SWAP', 'FIL-USDT-SWAP', 'LINK-USDT-SWAP', 'WLD-USDT-SWAP', 'UNI-USDT-SWAP', 'HYPE-USDT-SWAP', 'TRX-USDT-SWAP', 'WCT-USDT-SWAP', 'ETH-USDC-SWAP', 'XRP-USD-SWAP', 'ONDO-USDT-SWAP', 'OP-USDT-SWAP', 'MOODENG-USDT-SWAP', 'WIF-USDT-SWAP', 'FARTCOIN-USDT-SWAP', 'DOT-USDT-SWAP', 'ETC-USDT-SWAP', 'LTC-USD-SWAP', 'SHIB-USDT-SWAP', 'KAITO-USDT-SWAP', 'ALCH-USDT-SWAP', 'CRV-USDT-SWAP', 'TRB-USDT-SWAP', 'PI-USDT-SWAP', 'LDO-USDT-SWAP', 'PNUT-USDT-SWAP', 'PEOPLE-USDT-SWAP', 'ORDI-USDT-SWAP', 'FIL-USD-SWAP', 'NEAR-USDT-SWAP', 'APT-USDT-SWAP', 'ARB-USDT-SWAP', 'JUP-USDT-SWAP', 'TIA-USDT-SWAP', 'ETHFI-USDT-SWAP', 'MASK-USDT-SWAP', 'HBAR-USDT-SWAP', 'INJ-USDT-SWAP', 'XAUT-USDT-SWAP', 'ATH-USDT-SWAP', 'POL-USDT-SWAP', 'XLM-USDT-SWAP', 'ATOM-USDT-SWAP', 'SATS-USDT-SWAP', 'ADA-USD-SWAP', 'VIRTUAL-USDT-SWAP', 'CORE-USDT-SWAP', 'VINE-USDT-SWAP', 'IP-USDT-SWAP', 'LAYER-USDT-SWAP', 'BONK-USDT-SWAP', 'OM-USDT-SWAP', 'ETC-USD-SWAP', 'DYDX-USDT-SWAP', 'S-USDT-SWAP', 'SAND-USDT-SWAP', 'CFX-USDT-SWAP', 'NEIRO-USDT-SWAP', 'MKR-USDT-SWAP', 'ALGO-USDT-SWAP', 'LINK-USD-SWAP', 'GALA-USDT-SWAP', 'DOT-USD-SWAP', 'AIXBT-USDT-SWAP', 'CETUS-USDT-SWAP', 'PYTH-USDT-SWAP', 'GOAT-USDT-SWAP', 'NOT-USDT-SWAP', 'UNI-USD-SWAP', 'ACT-USDT-SWAP', 'JTO-USDT-SWAP', 'MERL-USDT-SWAP', 'BSV-USDT-SWAP', 'AI16Z-USDT-SWAP', 'MOVE-USDT-SWAP', 'ENS-USDT-SWAP', 'RENDER-USDT-SWAP', 'PENGU-USDT-SWAP', 'BERA-USDT-SWAP', 'SUSHI-USDT-SWAP', 'PROMPT-USDT-SWAP', 'FLM-USDT-SWAP', 'NEIROETH-USDT-SWAP', 'AUCTION-USDT-SWAP', 'HUMA-USDT-SWAP', 'ICP-USDT-SWAP', 'STRK-USDT-SWAP', 'POPCAT-USDT-SWAP', 'APE-USDT-SWAP', 'BOME-USDT-SWAP', 'IMX-USDT-SWAP', 'YGG-USDT-SWAP', 'TAO-USDT-SWAP', 'BABY-USDT-SWAP', 'TURBO-USDT-SWAP', 'RAY-USDT-SWAP', 'ZRO-USDT-SWAP', 'LPT-USDT-SWAP', 'MEW-USDT-SWAP', 'MEME-USDT-SWAP', 'LUNC-USDT-SWAP', 'AR-USDT-SWAP', 'UXLINK-USDT-SWAP', 'THETA-USDT-SWAP', 'SONIC-USDT-SWAP', 'ACH-USDT-SWAP', 'FLOKI-USDT-SWAP', 'STX-USDT-SWAP', 'SSV-USDT-SWAP', 'PARTI-USDT-SWAP', 'ANIME-USDT-SWAP', 'AXS-USDT-SWAP', 'JELLYJELLY-USDT-SWAP', 'BIGTIME-USDT-SWAP', 'X-USDT-SWAP', 'CRO-USDT-SWAP', 'INIT-USDT-SWAP', 'XTZ-USDT-SWAP', 'DOGS-USDT-SWAP', 'SOON-USDT-SWAP', 'COOKIE-USDT-SWAP', 'IOTA-USDT-SWAP', 'CATI-USDT-SWAP', 'ZEREBRO-USDT-SWAP', 'EIGEN-USDT-SWAP', 'MAGIC-USDT-SWAP', 'AVAX-USD-SWAP', 'CHZ-USDT-SWAP', 'ZETA-USDT-SWAP', 'W-USDT-SWAP', 'BCH-USD-SWAP', 'ETHW-USDT-SWAP', 'GRT-USDT-SWAP', 'CVC-USDT-SWAP', 'OL-USDT-SWAP', 'NEO-USDT-SWAP', 'ME-USDT-SWAP', 'YFI-USDT-SWAP', 'DUCK-USDT-SWAP', 'COMP-USDT-SWAP', 'BLUR-USDT-SWAP', 'DOOD-USDT-SWAP', 'ARKM-USDT-SWAP', 'DOG-USDT-SWAP', 'GRASS-USDT-SWAP', 'MANA-USDT-SWAP', 'LOOKS-USDT-SWAP', 'TRX-USD-SWAP', 'DEGEN-USDT-SWAP', 'API3-USDT-SWAP', 'ZIL-USDT-SWAP', 'ARC-USDT-SWAP', 'GMT-USDT-SWAP', 'STORJ-USDT-SWAP', 'NC-USDT-SWAP', 'RSR-USDT-SWAP', 'METIS-USDT-SWAP', 'FLOW-USDT-SWAP', 'QTUM-USDT-SWAP', 'ZRX-USDT-SWAP', 'SNX-USDT-SWAP', 'NIL-USDT-SWAP', '1INCH-USDT-SWAP', 'BIO-USDT-SWAP', 'AEVO-USDT-SWAP', 'PRCL-USDT-SWAP', 'USTC-USDT-SWAP', 'AIDOGE-USDT-SWAP', 'MORPHO-USDT-SWAP', 'CELO-USDT-SWAP', 'FXS-USDT-SWAP', 'VANA-USDT-SWAP', 'MINA-USDT-SWAP', 'HMSTR-USDT-SWAP', 'CSPR-USDT-SWAP', 'AVAAI-USDT-SWAP', 'XCH-USDT-SWAP', 'WOO-USDT-SWAP', 'SHELL-USDT-SWAP', 'EGLD-USDT-SWAP', 'SWARMS-USDT-SWAP', 'GAS-USDT-SWAP', 'MAJOR-USDT-SWAP', 'GRIFFAIN-USDT-SWAP', 'AGLD-USDT-SWAP', 'JST-USDT-SWAP', 'SUI-USD-SWAP', 'ATOM-USD-SWAP', 'J-USDT-SWAP', 'SIGN-USDT-SWAP', 'CVX-USDT-SWAP', 'CAT-USDT-SWAP', 'ALPHA-USDT-SWAP', 'UMA-USDT-SWAP', 'ACE-USDT-SWAP', 'RDNT-USDT-SWAP', 'TNSR-USDT-SWAP', 'GODS-USDT-SWAP', 'BAT-USDT-SWAP', 'XLM-USD-SWAP', 'CTC-USDT-SWAP', 'KSM-USDT-SWAP', 'RVN-USDT-SWAP', 'SLERF-USDT-SWAP', 'ONT-USDT-SWAP', 'BRETT-USDT-SWAP', 'BADGER-USDT-SWAP', 'ALGO-USD-SWAP', 'ONE-USDT-SWAP', 'SCR-USDT-SWAP', 'PIPPIN-USDT-SWAP', 'ICX-USDT-SWAP', 'LQTY-USDT-SWAP', 'T-USDT-SWAP', 'WAL-USDT-SWAP', 'USDC-USDT-SWAP', 'GMX-USDT-SWAP', 'PERP-USDT-SWAP', 'SAND-USD-SWAP', 'LRC-USDT-SWAP', 'IOST-USDT-SWAP', 'GLM-USDT-SWAP', 'BICO-USDT-SWAP', 'ID-USDT-SWAP', 'NMR-USDT-SWAP', 'SWEAT-USDT-SWAP', 'KNC-USDT-SWAP', 'BNT-USDT-SWAP', 'MOVR-USDT-SWAP', 'JOE-USDT-SWAP', 'TON-USD-SWAP', 'WAXP-USDT-SWAP', 'BAL-USDT-SWAP', 'GUN-USDT-SWAP', 'BAND-USDT-SWAP', 'DGB-USDT-SWAP', 'PLUME-USDT-SWAP', 'BR-USDT-SWAP', 'SLP-USDT-SWAP', 'PUFFER-USDT-SWAP', 'ZENT-USDT-SWAP', 'ORBS-USDT-SWAP', 'LSK-USDT-SWAP', 'SWELL-USDT-SWAP', 'ZK-USDT-SWAP', 'SOLV-USDT-SWAP', 'GPS-USDT-SWAP', 'SUNDOG-USDT-SWAP', 'LUNA-USDT-SWAP', 'OP-USD-SWAP', 'ENJ-USDT-SWAP', 'SOPH-USDT-SWAP']  # Add more as needed

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Timezone for alert timestamp
PH_TZ = pytz.timezone('Asia/Manila')

# Initialize OKX exchange
exchange = ccxt.okx({'enableRateLimit': True})
exchange.load_markets()

# Get OHLCV data
def get_ohlcv(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Check MACD cross
def get_macd_cross(df):
    macd_line, signal_line, _ = talib.MACD(df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    recent_macd = macd_line.iloc[-2:]
    recent_signal = signal_line.iloc[-2:]
    cross_up = recent_macd.iloc[-2] < recent_signal.iloc[-2] and recent_macd.iloc[-1] > recent_signal.iloc[-1]
    cross_down = recent_macd.iloc[-2] > recent_signal.iloc[-2] and recent_macd.iloc[-1] < recent_signal.iloc[-1]
    return cross_up, cross_down

# Check RSI
def get_rsi(df, period=30):
    rsi = talib.RSI(df['close'], timeperiod=period)
    return rsi

# Send alert to Discord
def send_discord_alert(symbol):
    now = datetime.now(PH_TZ).strftime('%Y-%m-%d %H:%M:%S')
    message = {
        "content": f"🔔 **ALERT**: `{symbol}`\n✅ 1H MACD crossed up\n✅ 15m RSI(30) > 50\n✅ 15m MACD crossed down\n🕒 `{now}`"
    }
    requests.post(DISCORD_WEBHOOK_URL, json=message)

# Main logic
for symbol in SYMBOLS:
    try:
        logging.info(f"Checking {symbol}...")

        df_1h = get_ohlcv(symbol, '1h')
        df_15m = get_ohlcv(symbol, '15m')

        # 1H MACD Cross Above
        macd_up_1h, _ = get_macd_cross(df_1h)
        if not macd_up_1h:
            logging.info(f"{symbol} - No 1H MACD cross above.")
            continue

        # 15m RSI > 50 or crosses above
        rsi_15m = get_rsi(df_15m)
        if rsi_15m.iloc[-1] < 50 and not (rsi_15m.iloc[-2] < 50 and rsi_15m.iloc[-1] > 50):
            logging.info(f"{symbol} - 15m RSI(30) not above or crossing above 50.")
            continue

        # 15m MACD Cross Below
        _, macd_down_15m = get_macd_cross(df_15m)
        if not macd_down_15m:
            logging.info(f"{symbol} - No 15m MACD cross below.")
            continue

        # All conditions met
        logging.info(f"{symbol} - 🔔 All conditions met!")
        send_discord_alert(symbol)

    except Exception as e:
        logging.error(f"Error with {symbol}: {e}")
