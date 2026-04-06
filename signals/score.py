import pandas as pd

def calculate_score(df: pd.DataFrame, cross_type: str) -> tuple[int, str]:
    df = df.copy()

    # RSI
    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_value = rsi.iloc[-1]

    # Volumen relativo (hoy vs promedio 20 días)
    vol_ratio = df["Volume"].iloc[-1] / df["Volume"].rolling(20).mean().iloc[-1]

    # Distancia entre EMAs (%)
    ema50 = df["Close"].ewm(span=50, adjust=False).mean().iloc[-1]
    ema200 = df["Close"].ewm(span=200, adjust=False).mean().iloc[-1]
    ema_gap = abs(ema50 - ema200) / ema200 * 100

    # Scoring
    if cross_type == "golden":
        rsi_score = 33 if rsi_value > 55 else 20 if rsi_value > 45 else 10
    else:
        rsi_score = 33 if rsi_value < 45 else 20 if rsi_value < 55 else 10

    vol_score = 33 if vol_ratio > 1.5 else 20 if vol_ratio > 1.0 else 10

    gap_score = 33 if ema_gap > 2 else 20 if ema_gap > 0.5 else 10

    total = rsi_score + vol_score + gap_score

   if total >= 80:
        label = "🔥 Very strong"
    elif total >= 60:
        label = "✅ Moderate"
    else:
        label = "⚠️ Weak"

    return total, label