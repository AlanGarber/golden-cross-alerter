import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from io import BytesIO

def generate_chart(df, symbol: str, cross_type: str) -> BytesIO:
    df = df.copy().tail(300)
    df["ma50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["ma200"] = df["Close"].ewm(span=200, adjust=False).mean()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df["Close"], label="Precio", color="#aaaaaa", linewidth=1)
    ax.plot(df.index, df["ma50"], label="MA50", color="#f0a500", linewidth=1.5)
    ax.plot(df.index, df["ma200"], label="MA200", color="#3a86ff", linewidth=1.5)

    color = "#f0a500" if cross_type == "golden" else "#ff4444"
    title = f"{'🟡 Golden Cross' if cross_type == 'golden' else '⚫ Death Cross'} — {symbol}"
    ax.set_title(title, fontsize=13, color=color)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=150)
    plt.close()
    buf.seek(0)
    return buf