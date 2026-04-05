# 📈 Golden Cross Alerter

Detecta **Golden Cross** y **Death Cross** en 500+ activos y envía alertas por Telegram automáticamente cada día hábil.

## ¿Cómo funciona?

1. Corre todos los días a las 18:00 EST via GitHub Actions
2. Descarga datos históricos con `yfinance`
3. Calcula MA50 y MA200
4. Si detecta un cruce, manda alerta por Telegram

## Ejemplo de alerta
🟡 GOLDEN CROSS — AAPL
🏢 Apple Inc.
💵 Precio: $189.42
📊 MA50:  $182.10
📊 MA200: $179.65
⚡ Señal de tendencia alcista 📈

