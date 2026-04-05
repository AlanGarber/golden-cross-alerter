import json
import os
from datetime import date

ALERTS_FILE = "db/alerts.json"

def load_alerts() -> dict:
    if not os.path.exists(ALERTS_FILE):
        return {}
    with open(ALERTS_FILE, "r") as f:
        return json.load(f)

def already_sent(symbol: str, cross_type: str) -> bool:
    alerts = load_alerts()
    key = f"{symbol}_{cross_type}"
    today = str(date.today())
    return alerts.get(key) == today

def mark_as_sent(symbol: str, cross_type: str):
    alerts = load_alerts()
    key = f"{symbol}_{cross_type}"
    alerts[key] = str(date.today())
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f)