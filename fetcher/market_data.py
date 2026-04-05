import yfinance as yf
import pandas as pd

def get_historical_data(symbol: str, period: str = "2y") -> pd.DataFrame:
    """
    Descarga datos históricos de un símbolo.
    Retorna un DataFrame con columna 'Close'.
    """
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)

    if df.empty:
        raise ValueError(f"No se encontraron datos para {symbol}")

    return df