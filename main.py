from dotenv import load_dotenv
load_dotenv()

from fetcher.market_data import get_historical_data, get_sp500_symbols
from signals.crossover import detect_crossover
from signals.score import calculate_score
from signals.backtest import get_historical_performance
from notifier.telegram_bot import notify_with_chart
from notifier.chart import generate_chart
from db.sent_alerts import already_sent, mark_as_sent
import yfinance as yf

EXTRA_SYMBOLS = ["BTC-USD", "ETH-USD", "SOL-USD", "SPY", "QQQ", "GLD"]

def get_company_name(symbol: str) -> str:
    try:
        return yf.Ticker(symbol).info.get("longName", symbol)
    except:
        return symbol

def build_caption(symbol: str, cross_type: str, df) -> str:
    price = df["Close"].iloc[-1]
    ema50 = df["Close"].ewm(span=50, adjust=False).mean().iloc[-1]
    ema200 = df["Close"].ewm(span=200, adjust=False).mean().iloc[-1]
    name = get_company_name(symbol)
    score, label = calculate_score(df, cross_type)
    perf = get_historical_performance(df, cross_type)

    emoji = "🟡" if cross_type == "golden" else "⚫"
    title = "GOLDEN CROSS" if cross_type == "golden" else "DEATH CROSS"
    trend = "bullish 📈" if cross_type == "golden" else "bearish 📉"

    caption = (
        f"{emoji} <b>{title} — {symbol}</b>\n"
        f"🏢 {name}\n\n"
        f"💵 Price: <b>${price:.2f}</b>\n"
        f"📊 EMA50:  <b>${ema50:.2f}</b>\n"
        f"📊 EMA200: <b>${ema200:.2f}</b>\n\n"
        f"⚡ Trend signal: {trend}\n\n"
        f"🎯 Confidence score: <b>{score}/100</b> — {label}\n"
        f"<i>RSI momentum + volume vs avg + EMA gap</i>\n\n"
    )

    if perf:
        if cross_type == "golden":
            caption += (
                f"📜 <b>Golden Cross history for {symbol}</b>\n"
                f"🔢 Previous signals: <b>{perf['total']}</b>\n"
                f"📈 Avg return 30d after signal: <b>{perf['avg_return']:+.1f}%</b>"
            )
        else:
            caption += (
                f"📜 <b>Death Cross history for {symbol}</b>\n"
                f"🔢 Previous signals: <b>{perf['total']}</b>\n"
                f"📉 Avg drop 30d after signal: <b>{abs(perf['avg_return']):.1f}%</b>"
            )
    else:
        caption += "📜 No previous signals found for this symbol"

    return caption

def run():
    symbols = get_sp500_symbols() + EXTRA_SYMBOLS
    print(f"Analizando {len(symbols)} símbolos...")

    for symbol in symbols:
        try:
            df = get_historical_data(symbol)
            result = detect_crossover(df)

            if result in ("golden", "death"):
                if already_sent(symbol, result):
                    print(f"⏭️ Ya enviado hoy: {symbol} {result}")
                    continue
                caption = build_caption(symbol, result, df)
                chart = generate_chart(df, symbol, result)
                print(caption)
                notify_with_chart(chart, caption)
                mark_as_sent(symbol, result)
            else:
                print(f"➖ Sin cruce en {symbol}")
        except Exception as e:
            print(f"⚠️ Error en {symbol}: {e}")

if __name__ == "__main__":
    run()