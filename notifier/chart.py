import mplfinance as mpf
import pandas as pd
from io import BytesIO

def generate_chart(df, symbol: str, cross_type: str) -> BytesIO:
    df = df.copy()
    df["ma50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["ma200"] = df["Close"].ewm(span=200, adjust=False).mean()

    df_plot = df.copy()
    df_plot.index = df_plot.index.tz_localize(None)

    # Detectar cruces históricos (menos el último)
    # Detectar todos los cruces históricos (menos el último)
    cross_dates = []
    for i in range(1, len(df_plot) - 1):
        yesterday = df_plot.iloc[i - 1]
        today = df_plot.iloc[i]

        golden = yesterday["ma50"] < yesterday["ma200"] and today["ma50"] > today["ma200"]
        death = yesterday["ma50"] > yesterday["ma200"] and today["ma50"] < today["ma200"]

        if golden or death:
            cross_dates.append(i)

    apds = [
        mpf.make_addplot(df_plot["ma50"], color="#f0a500", width=1.5, label="EMA50"),
        mpf.make_addplot(df_plot["ma200"], color="#3a86ff", width=1.5, label="EMA200"),
    ]

    title = f"{'Golden Cross' if cross_type == 'golden' else 'Death Cross'} — {symbol}"

    buf = BytesIO()
    fig, axes = mpf.plot(
        df_plot,
        type="candle",
        style="charles",
        title=title,
        addplot=apds,
        figsize=(14, 6),
        warn_too_much_data=10000,
        returnfig=True,
    )

    # Marcar cruces históricos con línea vertical
    line_color = "#f0a500" if cross_type == "golden" else "#ff4444"
    for idx in cross_dates:
        axes[0].axvline(x=idx, color=line_color, linewidth=1, linestyle="--", alpha=0.7)

    fig.savefig(buf, format="png", dpi=150)
    buf.seek(0)
    return buf