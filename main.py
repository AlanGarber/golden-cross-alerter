from dotenv import load_dotenv
load_dotenv()

from fetcher.market_data import get_historical_data
from signals.crossover import detect_crossover
from notifier.telegram_bot import notify

SYMBOLS = ["AAPL", "BTC-USD", "NVDA"]

def run():
    for symbol in SYMBOLS:
        print(f"Analizando {symbol}...")
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
        else:
            print(f"➖ Sin cruce en {symbol}")

if __name__ == "__main__":
    run()