import mplfinance as mpf
from io import BytesIO

def generate_chart(df, symbol: str, cross_type: str) -> BytesIO:
    df = df.copy()
    df["ma50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["ma200"] = df["Close"].ewm(span=200, adjust=False).mean()

    df_plot = df.tail(126).copy()
    df_plot.index = df_plot.index.tz_localize(None)

    apds = [
        mpf.make_addplot(df_plot["ma50"], color="#f0a500", width=1.5, label="EMA50"),
        mpf.make_addplot(df_plot["ma200"], color="#3a86ff", width=1.5, label="EMA200"),
    ]

    title = f"{'Golden Cross' if cross_type == 'golden' else 'Death Cross'} — {symbol}"

    buf = BytesIO()
    mpf.plot(
        df_plot,
        type="candle",
        style="charles",
        title=title,
        addplot=apds,
        figsize=(12, 6),
        savefig=dict(fname=buf, format="png", dpi=150),
    )
    buf.seek(0)
    return buf