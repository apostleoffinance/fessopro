import pendulum as dt
import pandas as pd
from datetime import datetime, timedelta
import time
import logging
import pandas_ta as ta

# Alpaca trading & data imports
from alpaca.trading.requests import GetOrdersRequest, MarketOrderRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus, TimeInForce
from alpaca.data.historical import CryptoHistoricalDataClient
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import CryptoBarsRequest
from alpaca.trading.client import TradingClient

from dotenv import load_dotenv
import os

# ===========================
# LOAD API CREDENTIALS & SETUP LOGGING
# ===========================
# Load environment variables containing API keys
load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

# Initialize Alpaca trading client in paper trading mode
trading_client = TradingClient(api_key, secret_key, paper=True)

# Define tickers, timezone, and strategy name for logging
list_of_tickers = ["ETH/USD", 'AAVE/USD']
time_zone = 'America/New_York'
strategy_name = 'crypto_sma'

# Setup logging to file with timestamp
logging.basicConfig(level=logging.INFO,
                    filename=f'{strategy_name}_{dt.now(tz=time_zone).date()}.log',
                    filemode='a',
                    format="%(asctime)s - %(message)s")
logging.info(f'starting {strategy_name} strategy file')

# ===========================
# HISTORICAL DATA FETCHING FUNCTION
# ===========================
def get_historical_crypto_data(ticker, duration, time_frame_unit):
    """
    Fetch historical crypto data (bars) for a given ticker and timeframe.
    Adds SMA(20) and SMA(50) indicators to the data for strategy logic.
    """
    crypto_historical_data_client = CryptoHistoricalDataClient()
    now = dt.now(tz=time_zone)
    req = CryptoBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame(amount=1, unit=time_frame_unit),
        start=now - dt.duration(days=duration)
    )

    history_df1 = crypto_historical_data_client.get_crypto_bars(req).df
    # Clean and reformat data
    sdata = history_df1.reset_index().drop('symbol', axis=1)
    sdata['timestamp'] = sdata['timestamp'].dt.tz_convert('America/New_York')
    sdata = sdata.set_index('timestamp')

    # Calculate 20-period and 50-period simple moving averages
    sdata['sma_20'] = ta.sma(sdata['close'], length=20)
    sdata['sma_50'] = ta.sma(sdata['close'], length=50)

    return sdata

# ===========================
# ACCOUNT / ORDER MANAGEMENT
# ===========================
def get_all_open_orders():
    """Fetches all currently open orders and returns them as a filtered DataFrame."""
    request_params = GetOrdersRequest(status=QueryOrderStatus.OPEN)
    orders = trading_client.get_orders(filter=request_params)
    order_df = pd.DataFrame([dict(elem) for elem in orders])

    # Filter orders for only tickers in our watchlist
    order_df = order_df[order_df['symbol'].isin(list_of_tickers)]
    order_df.to_csv('orders1.csv')
    return order_df

def get_all_position():
    """Fetches all open positions and returns them as a filtered DataFrame."""
    pos = trading_client.get_all_positions()
    pos_df = pd.DataFrame([dict(elem) for elem in pos])
    pos_df = pos_df[pos_df['symbol'].str.replace('/', '').isin([i.replace('/', '') for i in list_of_tickers])]
    pos_df.to_csv('position1.csv')
    return pos_df

# Immediately log current positions when script starts
get_all_position()

# ===========================
# ORDER / POSITION CLOSING UTILITIES
# ===========================
def close_this_position(ticker_name):
    """Closes a specific open position if it exists."""
    ticker_name = ticker_name.replace('/', '')
    try:
        c = trading_client.close_position(ticker_name)
        print(c)
        print('position closed')
    except:
        print('position does not exist')

def close_this_order(ticker_name):
    """Cancels a specific open order if it exists."""
    try:
        for i in trading_client.get_orders():
            if i.symbol == ticker_name:
                trading_client.cancel_order_by_id(i.id)
                print('closed order for ', ticker_name)
    except:
        print('order does not exist')

def close_all_position():
    """Closes all positions in the watchlist."""
    for ticker1 in list_of_tickers:
        close_this_position(ticker1)

def close_all_orders():
    """Cancels all open orders in the watchlist."""
    for ticker1 in list_of_tickers:
        close_this_order(ticker1)

# ===========================
# ORDER PLACEMENT FUNCTION
# ===========================
def trade_buy_stocks(ticker, closing_price):
    """
    Places a market buy order for the given ticker using Alpaca API.
    Currently hardcoded to buy a quantity of 1.
    """
    print('placing market order')
    market_order_data = MarketOrderRequest(
        symbol=ticker,
        qty=1,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC
    )
    market_order = trading_client.submit_order(order_data=market_order_data)
    print(market_order)
    print('done placing market order for ', ticker)

# ===========================
# STRATEGY LOGIC
# ===========================
def strategy(hist_df, ticker):
    """
    Core strategy logic:
    - Buys when SMA(20) crosses above SMA(50) (bullish crossover).
    - Allocates 1/3 of available cash to the trade.
    """
    buy_condition = (hist_df['sma_20'].iloc[-1] > hist_df['sma_50'].iloc[-1]) and \
                    (hist_df['sma_20'].iloc[-2] < hist_df['sma_50'].iloc[-2])

    money = float(trading_client.get_account().cash) / 3
    closing_price = hist_df['close'].iloc[-1]

    # Only trade if we have enough capital for at least 1 unit
    if money > closing_price:
        if buy_condition:
            trade_buy_stocks(ticker, closing_price)
        else:
            print('no condition satisfied')
    else:
        print('we dont have enough money to trade')

# ===========================
# MAIN STRATEGY EXECUTION LOOP
# ===========================
def main_strategy_code():
    """
    Executes the strategy:
    - Fetches open orders & positions
    - Fetches fresh historical data & indicators
    - Calculates quantity size
    - Applies buy/sell logic depending on whether we have a position
    """
    ord_df = get_all_open_orders()
    pos_df = get_all_position()

    for ticker in list_of_tickers:
        hist_df = get_historical_crypto_data(ticker, 2, TimeFrameUnit.Minute)
        money = float(trading_client.get_account().cash) / 3
        ltp = hist_df['close'].iloc[-1]
        quantity = money // ltp

        # Skip ticker if quantity would be zero
        if quantity == 0:
            continue

        # If we have no positions, check for buy opportunities
        if pos_df.empty:
            strategy(hist_df, ticker)

        # If we have positions but not for this ticker, still check for buy opportunities
        elif ticker.replace('/', '') not in pos_df['symbol'].to_list():
            strategy(hist_df, ticker)

        # If we have a position in this ticker, check whether to sell
        else:
            curr_quant = float(pos_df[pos_df['symbol'] == ticker.replace('/', '')]['qty'].iloc[-1])
            if curr_quant > 0:
                sell_condition = (hist_df['sma_20'].iloc[-1] < hist_df['sma_50'].iloc[-1]) and \
                                 (hist_df['sma_20'].iloc[-2] > hist_df['sma_50'].iloc[-2])
                if sell_condition:
                    close_this_position(ticker)

# ===========================
# TIME-BASED EXECUTION CONTROL
# ===========================
# Define trading window (start and end time)
current_time = dt.now(tz=time_zone)
start_hour, start_min = 4, 36
end_hour, end_min = 5, 20

start_time = dt.datetime(current_time.year, current_time.month, current_time.day,
                         start_hour, start_min, tz=time_zone)
end_time = dt.datetime(current_time.year, current_time.month, current_time.day,
                       end_hour, end_min, tz=time_zone)

# Wait until start time before running strategy
while dt.now(tz=time_zone) < start_time:
    time.sleep(1)

# Main trading loop - runs until end time is reached
while True:
    if dt.now(tz=time_zone) > end_time:
        break
    ct = dt.now(tz=time_zone)

    # Run strategy once every minute when seconds == 2
    if ct.second == 2:
        main_strategy_code()

    time.sleep(1)

print('strategy stopped')
