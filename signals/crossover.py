import pandas as pd

def detect_crossover(df: pd.DataFrame) -> str | None:
    """
    Recibe un DataFrame con columna 'Close' y al menos 200 filas.
    Retorna: 'golden', 'death', o None si no hubo cruce hoy.
    """
    df = df.copy()
    df["ma50"] = df["Close"].rolling(window=50).mean() #Media móvil de 50 días
    df["ma200"] = df["Close"].rolling(window=200).mean() #Media móvil de 200 días

    today = df.iloc[-1] #Ultima fila de dataframe (Hoy)
    yesterday = df.iloc[-2] #Anteultima fila de dataframe (Ayer)

    golden = yesterday["ma50"] < yesterday["ma200"] and today["ma50"] > today["ma200"] #Cruce al alza
    death = yesterday["ma50"] > yesterday["ma200"] and today["ma50"] < today["ma200"] #Cruce a la baja

    if golden:
        return "golden"
    elif death:
        return "death"
    return None