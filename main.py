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
    trend = "alcista 📈" if cross_type == "golden" else "bajista 📉"

    caption = (
        f"{emoji} <b>{title} — {symbol}</b>\n"
        f"🏢 {name}\n\n"
        f"💵 Precio: <b>${price:.2f}</b>\n"
        f"📊 EMA50:  <b>${ema50:.2f}</b>\n"
        f"📊 EMA200: <b>${ema200:.2f}</b>\n\n"
        f"⚡ Señal de tendencia {trend}\n\n"
        f"🎯 Score de confianza: <b>{score}/100</b> — {label}\n\n"
    )

    if perf:
        tipo = "Golden Cross" if cross_type == "golden" else "Death Cross"
        direccion = "subió" if cross_type == "golden" else "bajó"
        caption += (
            f"📜 <b>Historial de {tipo} en {symbol}</b>\n"
            f"🔢 Señales previas: <b>{perf['total']}</b>\n"
            f"✅ Win rate: <b>{perf['win_rate']:.1f}%</b> "
            f"(veces que {direccion} en 30d)\n"
            f"📈 Retorno promedio 30d: <b>{perf['avg_return']:+.1f}%</b>\n"
            f"🏆 Mejor caso: <b>{perf['best']:+.1f}%</b>\n"
            f"💀 Peor caso: <b>{perf['worst']:+.1f}%</b>"
        )
    else:
        caption += "📜 Sin historial previo para este símbolo"

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