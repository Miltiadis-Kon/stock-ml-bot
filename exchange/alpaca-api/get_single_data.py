#Retrieve historical data for a single symbol from Alpaca API 

from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

# no keys required for crypto data
client = CryptoHistoricalDataClient()

def get_crypto_bars(ticket, start, end):
    request = CryptoBarsRequest(
        symbol_or_symbols=ticket,
        timeframe=TimeFrame.Minute,
        start=start,
        end=end
    )
    bars = client.get_crypto_bars(request)
    return bars[ticket]

def convert_into_chart_data(data):
    chart_data = []
    for bar in data:
        chart_data.append({
            "time": bar.timestamp,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume
        })
    return chart_data

def convert_into_xmin(chart_data,t):
    chart_data_5min = []
    for i in range(0, len(chart_data), t):
        if i + t < len(chart_data):
            chart_data_5min.append({
                "time": chart_data[i]["time"],
                "open": chart_data[i]["open"],
                "high": max([x["high"] for x in chart_data[i:i+t]]),
                "low": min([x["low"] for x in chart_data[i:i+t]]),
                "close": chart_data[i+t]["close"],
                "volume": sum([x["volume"] for x in chart_data[i:i+t]])
            })
    return chart_data_5min
