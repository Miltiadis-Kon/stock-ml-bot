import datetime
import pandas as pd
from lightweight_charts import Chart

import get_single_data 


def get_bar_data(symbol, timeframe):
    if timeframe == '1min':
        return df
    elif timeframe == '5min':
        return pd.DataFrame(get_single_data.convert_into_xmin(onemin_data,5))
    elif timeframe == '15min':
        return pd.DataFrame(get_single_data.convert_into_xmin(onemin_data,15))
    elif timeframe == '30min':
        return pd.DataFrame(get_single_data.convert_into_xmin(onemin_data,30))
    elif timeframe == '1h':
        return pd.DataFrame(get_single_data.convert_into_xmin(onemin_data,60))
    elif timeframe == '4h':
        return pd.DataFrame(get_single_data.convert_into_xmin(onemin_data,240))
    elif timeframe == '1d':
        return pd.DataFrame(get_single_data.convert_into_xmin(onemin_data,1440))
    else:
        return pd.DataFrame()


def on_search(chart, searched_string):  # Called when the user searches.
    new_data = get_bar_data(searched_string, chart.topbar['timeframe'].value)
    if new_data.empty:
        return
    chart.topbar['symbol'].set(searched_string)
    chart.set(new_data)


def on_timeframe_selection(chart):  # Called when the user changes the timeframe.
    new_data = get_bar_data(chart.topbar['symbol'].value, chart.topbar['timeframe'].value)
    if new_data.empty:
        return
    chart.set(new_data, True)


def on_horizontal_line_move(chart, line):
    print(f'Horizontal line moved to: {line.price}')


if __name__ == '__main__':
    # Define the start and end dates for the data 
    start = datetime.datetime.now() - datetime.timedelta(days=7)
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = datetime.datetime.now()
    ticket = "BTC/USD"
    data = get_single_data.get_crypto_bars(ticket, start, end) # Get the data from the API
    onemin_data = get_single_data.convert_into_chart_data(data) # Convert the data into 1 minute intervals
    df = pd.DataFrame(onemin_data) # Convert the data into a pandas dataframe

    chart = Chart(toolbox=True) # Create a new chart
    chart.legend(True) 

    chart.events.search += on_search

    chart.topbar.textbox('symbol', ticket)
    chart.topbar.switcher('timeframe', ('1min', '5min','15min', '30min','1h','4h','1d'), default='1min',
                          func=on_timeframe_selection)
    chart.set(df)

    chart.horizontal_line(200, func=on_horizontal_line_move)

    chart.show(block=True)
