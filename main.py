from fetcher.market_data import get_historical_data
from signals.crossover import detect_crossover

SYMBOLS = ["AAPL", "BTC-USD", "NVDA"]

def run():
    for symbol in SYMBOLS:
        print(f"Analizando {symbol}...")
        df = get_historical_data(symbol)
        result = detect_crossover(df)

        if result == "golden":
            print(f"🟡 GOLDEN CROSS detectado en {symbol}")
        elif result == "death":
            print(f"⚫ DEATH CROSS detectado en {symbol}")
        else:
            print(f"➖ Sin cruce en {symbol}")

if __name__ == "__main__":
    run()