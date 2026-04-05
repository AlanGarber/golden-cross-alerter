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

def get_sp500_symbols() -> list[str]:
    import requests
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url, headers=headers)
    df = pd.read_html(response.text)[0]
    return df["Symbol"].tolist()