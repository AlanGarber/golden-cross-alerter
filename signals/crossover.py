import pandas as pd

def detect_crossover(df: pd.DataFrame) -> str | None:
    """
    Recibe un DataFrame con columna 'Close' y al menos 200 filas.
    Retorna: 'golden', 'death', o None si no hubo cruce hoy.
    """
    df = df.copy()
    df["ma50"] = df["Close"].ewm(span=50, adjust=False).mean()
    df["ma200"] = df["Close"].ewm(span=200, adjust=False).mean()

    today = df.iloc[-1]
    yesterday = df.iloc[-2]

    golden = yesterday["ma50"] < yesterday["ma200"] and today["ma50"] > today["ma200"]
    death = yesterday["ma50"] > yesterday["ma200"] and today["ma50"] < today["ma200"]

    if golden:
        return "golden"
    elif death:
        return "death"
    return None