from dotenv import load_dotenv
load_dotenv()

from fetcher.market_data import get_historical_data, get_sp500_symbols
from signals.crossover import detect_crossover
from notifier.telegram_bot import notify_with_chart
from notifier.chart import generate_chart
import yfinance as yf

EXTRA_SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD", "SPY", "QQQ", "GLD"]

def get_company_name(symbol: str) -> str:
    try:
        return yf.Ticker(symbol).info.get("longName", symbol)
    except:
        return symbol

def build_caption(symbol: str, cross_type: str, df) -> str:
    price = df["Close"].iloc[-1]
    ma50 = df["Close"].ewm(span=50, adjust=False).mean().iloc[-1]
    ma200 = df["Close"].ewm(span=200, adjust=False).mean().iloc[-1]
    name = get_company_name(symbol)

    emoji = "🟡" if cross_type == "golden" else "⚫"
    title = "GOLDEN CROSS" if cross_type == "golden" else "DEATH CROSS"
    trend = "alcista 📈" if cross_type == "golden" else "bajista 📉"

    return (
        f"{emoji} <b>{title} — {symbol}</b>\n"
        f"🏢 {name}\n\n"
        f"💵 Precio: <b>${price:.2f}</b>\n"
        f"📊 MA50:  <b>${ma50:.2f}</b>\n"
        f"📊 MA200: <b>${ma200:.2f}</b>\n\n"
        f"⚡ Señal de tendencia {trend}"
    )

def run():
    symbols = get_sp500_symbols() + EXTRA_SYMBOLS
    print(f"Analizando {len(symbols)} símbolos...")

    for symbol in symbols:
        try:
            df = get_historical_data(symbol)
            result = detect_crossover(df)

            if result in ("golden", "death"):
                caption = build_caption(symbol, result, df)
                chart = generate_chart(df, symbol, result)
                print(caption)
                notify_with_chart(chart, caption)
            else:
                print(f"➖ Sin cruce en {symbol}")
        except Exception as e:
            print(f"⚠️ Error en {symbol}: {e}")

if __name__ == "__main__":
    run()