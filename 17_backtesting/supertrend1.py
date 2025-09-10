# Importing required libraries
from backtesting import Backtest, Strategy      # For running backtests on strategies
import yfinance as yf                           # To fetch historical stock data
import pandas as pd
import numpy as np
import pandas_ta as ta                           # Technical Analysis library for indicators like Supertrend

# ===========================
# 1. Fetch historical data
# ===========================
# Download historical OHLCV (Open, High, Low, Close, Volume) data for AMZN (Amazon) for the last 4 years
data = yf.download('AMZN', period='4y', multi_level_index=False)
print(data)  # Print data to verify it's loaded correctly

# ===========================
# 2. Calculate Supertrend using pandas_ta
# ===========================
# Using pandas_ta's built-in supertrend indicator for reference/comparison
s = ta.supertrend(data['High'], data['Low'], data['Close'])
print(s)

# ===========================
# 3. Custom Supertrend Function
# ===========================
def supertrend(high, low, close, length=10, multiplier=3):
    """
    Custom implementation of the Supertrend indicator.
    It calculates the same values as pandas_ta.supertrend but allows more flexibility and control.
    """

    # ---- Step 1: Calculate True Range (TR) ----
    tr1 = high - low                                # High - Low
    tr2 = abs(high - close.shift(1))                # |High - Previous Close|
    tr3 = abs(low - close.shift(1))                 # |Low - Previous Close|
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)  # Max of the three gives TR

    # ---- Step 2: Calculate ATR (Average True Range) using EMA (RMA) ----
    atr = true_range.ewm(alpha=1/length, adjust=False).mean()

    # ---- Step 3: Calculate basic upper/lower bands ----
    hl2 = (high + low) / 2
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    # ---- Step 4: Initialize trend direction ----
    direction = [1]  # Start with a "long" trend by default
    trend = [lowerband.iloc[0]]  # First trend value = lower band
    long = [lowerband.iloc[0]]   # Long signals
    short = [np.nan]             # Short signals start empty

    # ---- Step 5: Iteratively compute Supertrend ----
    for i in range(1, len(close)):
        # Update direction based on price crossing bands
        if close.iloc[i] > upperband.iloc[i - 1]:
            direction.append(1)  # Switch to long
        elif close.iloc[i] < lowerband.iloc[i - 1]:
            direction.append(-1) # Switch to short
        else:
            direction.append(direction[i - 1])  # Keep previous direction
            # Adjust bands to avoid sudden flip-flops
            if direction[i] == 1 and lowerband.iloc[i] < lowerband.iloc[i - 1]:
                lowerband.iloc[i] = lowerband.iloc[i - 1]
            if direction[i] == -1 and upperband.iloc[i] > upperband.iloc[i - 1]:
                upperband.iloc[i] = upperband.iloc[i - 1]

        # Append corresponding trend line values
        if direction[i] == 1:
            trend.append(lowerband.iloc[i])
            long.append(lowerband.iloc[i])
            short.append(np.nan)
        else:
            trend.append(upperband.iloc[i])
            long.append(np.nan)
            short.append(upperband.iloc[i])

    # ---- Step 6: Return as DataFrame ----
    df = pd.DataFrame({
        "SUPERT": trend,      # Supertrend line
        "SUPERTd": direction, # Trend direction: 1=long, -1=short
        "SUPERTl": long,      # Long-only values
        "SUPERTs": short,     # Short-only values
    }, index=close.index)

    return df

# Calculate Supertrend using custom function
s = supertrend(data['High'], data['Low'], data['Close'])
print(s)

# ===========================
# 4. Helper Functions for Strategy
# ===========================
def super1(high, low, close, l=10, m=3):
    """Returns just the Supertrend line (SUPERT)"""
    s = supertrend(high, low, close, l, m)
    return s['SUPERT']

def trend(high, low, close, l=10, m=3):
    """Returns just the trend direction (SUPERTd)"""
    s = supertrend(high, low, close, l, m)
    return s['SUPERTd']

# ===========================
# 5. Create Backtest Strategy
# ===========================
class Superstrategy(Strategy):
    # Strategy parameters
    l = 10  # ATR length
    m = 3   # ATR multiplier

    def init(self):
        """
        Called once at the start.
        Registers indicators to be used in the strategy.
        """
        self.super = self.I(super1, self.data.High.s, self.data.Low.s, self.data.Close.s, self.l, self.m)
        self.trend = self.I(trend, self.data.High.s, self.data.Low.s, self.data.Close.s, self.l, self.m)

    def next(self):
        """
        Called on every new candle (price bar).
        Contains the trading logic: buy/sell signals.
        """
        # BUY SIGNAL: Trend turns long (1) and we are not already long
        if self.trend[-1] == 1 and ((not self.position) or (self.position.is_short)):
            self.position.close()                      # Close any existing short position
            close = self.data.Close[-1]                # Get current close price
            self.buy(sl=0.95 * close)                  # Open long with stop-loss 5% below entry

        # SELL SIGNAL: Trend turns short (-1) and we are not already short
        elif self.trend[-1] == -1 and ((not self.position) or (self.position.is_long)):
            self.position.close()                      # Close any existing long position
            close = self.data.Close[-1]                # Get current close price
            self.sell(sl=1.05 * close)                 # Open short with stop-loss 5% above entry

# Test helper functions
print(super1(data['High'], data['Low'], data['Close']))
print(trend(data['High'], data['Low'], data['Close']))

# ===========================
# 6. Run Backtest
# ===========================
bt = Backtest(data, Superstrategy, cash=10_000, commission=.002)  # 0.2% commission
output = bt.run()  # Run backtest
print(output)
bt.plot()  # Visualize trades and equity curve

# ===========================
# 7. Optimize Parameters
# ===========================
output = bt.optimize(
    l=range(5, 50, 5),       # Try ATR lengths from 5 to 45
    m=range(2, 6, 1),        # Try multipliers from 2 to 5
    maximize='Return [%]'    # Find params that maximize total return
)
print(output)
print(output['_strategy'])  # Print optimized strategy parameters
bt.plot()
