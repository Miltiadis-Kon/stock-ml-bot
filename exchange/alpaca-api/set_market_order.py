# This script is used to set a market order on Alpaca API using the alpaca-python library.

# Get configuration data 
from config import trading_client # Import the trading client from the config file
# trading_client = TradingClient(alpacakey,alpacasecret, paper=paper)


from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, StopOrderRequest
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce,QueryOrderStatus


def getOrder(order):
    if order == "buy":
        return OrderSide.BUY
    else:
        return OrderSide.SELL 

# A market order is a request to buy or sell a security immediately at the best available current price.  
def submit_market_order(ticket, quantity, order):
    market_order_data = MarketOrderRequest(
                    symbol=ticket, # Ticker symbol
                    qty=quantity, # Quantity of the order
                    side=getOrder(order), # Buy order
                    time_in_force=TimeInForce.DAY if quantity < 1 else TimeInForce.GTC # Good till cancel
                    )

    market_order = trading_client.submit_order(
                order_data=market_order_data
               )
    print("[MARKET ORDER] " + market_order.side + " "+ market_order.qty +" $" + market_order.symbol)
    return market_order

# A limit order is a request to buy or sell a security at a specific price or better.
def submit_limit_order(ticket, quantity, order, limit_price):
    limit_order_data = LimitOrderRequest(
                    symbol=ticket, # Ticker symbol
                    qty=quantity, # Quantity of the order
                    side=getOrder(order), # Buy order
                    time_in_force=TimeInForce.DAY if quantity < 1 else TimeInForce.GTC, # Good till cancel
                    limit_price=limit_price
                    )

    limit_order = trading_client.submit_order(
                order_data=limit_order_data
               )
    print("[LIMIT ORDER] " + limit_order.side + " "+ limit_order.qty +" $" + limit_order.symbol + " at $" + limit_order.limit_price)
    return limit_order

# A stop order is an order type that is triggered when the price of a security reaches the stop price level set by the investor.
def submit_stop_order(ticket, quantity, order, stop_price):
    stop_order_data = StopOrderRequest(
                    symbol=ticket, # Ticker symbol
                    qty=quantity, # Quantity of the order
                    side=getOrder(order), # Buy order
                    time_in_force=TimeInForce.DAY if quantity < 1 else TimeInForce.GTC, # Good till cancel
                    stop_price=stop_price
                    )

    stop_order = trading_client.submit_order(
                order_data=stop_order_data
               )
    print("[STOP ORDER] " + stop_order.side + " "+ stop_order.qty +" $" + stop_order.symbol + " at $" + stop_order.stop_price)
    return stop_order


# EXAMPLES 
# Submit a market order
#submit_market_order("SPY", 2,"buy")
#submit_limit_order("AAPL", 0.1,"sell", 120)
#submit_stop_order("AAPL", 1,"sell", 110)
