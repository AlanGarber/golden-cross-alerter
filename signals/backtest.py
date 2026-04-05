import pandas as pd

def get_historical_performance(df: pd.DataFrame, cross_type: str, forward_days: int = 30) -> dict:
    df = df.copy()
    df["ema50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["Close"].ewm(span=200, adjust=False).mean()

    signals = []

    for i in range(1, len(df) - forward_days):
        yesterday = df.iloc[i - 1]
        today = df.iloc[i]

        golden = yesterday["ema50"] < yesterday["ema200"] and today["ema50"] > today["ema200"]
        death = yesterday["ema50"] > yesterday["ema200"] and today["ema50"] < today["ema200"]

        if (cross_type == "golden" and golden) or (cross_type == "death" and death):
            price_at_cross = today["Close"]
            price_after = df.iloc[i + forward_days]["Close"]
            pct_change = (price_after - price_at_cross) / price_at_cross * 100
            signals.append(pct_change)

    if not signals:
        return None

    wins = [s for s in signals if (s > 0 if cross_type == "golden" else s < 0)]

    return {
        "total": len(signals),
        "win_rate": len(wins) / len(signals) * 100,
        "avg_return": sum(signals) / len(signals),
        "best": max(signals),
        "worst": min(signals),
    }