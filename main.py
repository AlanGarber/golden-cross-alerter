from dotenv import load_dotenv
load_dotenv()

from fetcher.market_data import get_historical_data, get_sp500_symbols
from signals.crossover import detect_crossover
from notifier.telegram_bot import notify

EXTRA_SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD", "SPY", "QQQ", "GLD"]

def run():
    symbols = get_sp500_symbols() + EXTRA_SYMBOLS
    print(f"Analizando {len(symbols)} símbolos...")

    for symbol in symbols:
        try:
            df = get_historical_data(symbol)
            result = detect_crossover(df)

            if result == "golden":
                msg = f"🟡 GOLDEN CROSS detectado en {symbol}"
                print(msg)
                notify(msg)
            elif result == "death":
                msg = f"⚫ DEATH CROSS detectado en {symbol}"
                print(msg)
                notify(msg)
        except Exception as e:
            print(f"⚠️ Error en {symbol}: {e}")

if __name__ == "__main__":
    run()