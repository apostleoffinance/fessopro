# ===============================
# IMPORT REQUIRED LIBRARIES
# ===============================
from backtesting import Strategy, Backtest       # Backtesting framework to simulate trades
import yfinance as yf                            # To download historical market data
import pandas_ta as ta                           # Technical indicators like Supertrend & EMA
from backtesting.lib import resample_apply        # To resample data (e.g., hourly → daily)
import time

# ===============================
# DEFINE INDICATOR FUNCTIONS
# ===============================
def supertrend1(high_data, low_data, close_data, l):
    """
    Function to calculate the Supertrend direction (SUPERTd) using pandas_ta.
    Returns +1 for uptrend and -1 for downtrend.
    """
    o = ta.supertrend(high_data, low_data, close_data, length=l)
    return o[f'SUPERTd_{l}_3.0']  # Extract the trend direction column

def supertrend2(high_data, low_data, close_data, l):
    """
    Function to calculate the Supertrend value (SUPERT) using pandas_ta.
    Returns the supertrend line itself.
    """
    o = ta.supertrend(high_data, low_data, close_data, length=l)
    return o[f'SUPERT_{l}_3.0']  # Extract the supertrend line

def ema(close_data, period=9):
    """
    Function to calculate the Exponential Moving Average (EMA).
    Returns EMA of closing prices.
    """
    return ta.ema(close_data, length=period)


# ===============================
# CREATE STRATEGY CLASS
# ===============================
class supertrend_ema(Strategy):
    """
    A strategy that combines Supertrend with a higher timeframe EMA filter.
    Buy when:
        - Supertrend shows uptrend
        - Price is above daily EMA
    Sell when:
        - Supertrend shows downtrend
        - Price is below daily EMA
    """
    super_length = 30   # ATR period for Supertrend
    ema_length = 10     # EMA period

    def init(self):
        """
        Called once at the beginning of the backtest.
        Initializes indicators and attaches them to the Strategy instance.
        """
        # Calculate Supertrend signals on the original timeframe (hourly data)
        self.super1 = self.I(supertrend1, self.data.High.s, self.data.Low.s, self.data.Close.s, self.super_length)
        self.super2 = self.I(supertrend2, self.data.High.s, self.data.Low.s, self.data.Close.s, self.super_length)

        # Calculate EMA on resampled (daily) data for trend confirmation
        self.daily_ema = resample_apply('D', ema, self.data.Close.s, self.ema_length)

    def next(self):
        """
        Called for each new candle (bar).
        Contains trading logic: Entry & Exit rules.
        """
        # ---- BUY CONDITIONS ----
        if self.super1[-1] > 0 and self.data.Close[-1] > self.daily_ema[-1]:
            # If currently short, close the short position first
            if self.position.is_short:
                self.position.close()
            # If not already in a trade, open a long position
            if not self.position:
                self.buy(size=0.95)  # Use 95% of available cash for the trade

        # ---- SELL CONDITIONS ----
        elif self.super1[-1] < 0 and self.data.Close[-1] < self.daily_ema[-1]:
            # If currently long, close the long position first
            if self.position.is_long:
                self.position.close()
            # If not already in a trade, open a short position
            if not self.position:
                self.sell(size=0.95)  # Use 95% of available cash for the trade


# ===============================
# FETCH HISTORICAL DATA
# ===============================
# Download NIFTY 50 (^NSEI) hourly data for the last ~700 days
data = yf.download('^NSEI', period='700d', interval='1h')

# Convert timestamp from UTC to IST (India Standard Time)
data.index = data.index.tz_convert('Asia/Kolkata')

# Flatten column MultiIndex (if present) to simple column names
data.columns = [c[0] for c in data.columns]
print(data.head())

# ===============================
# TEST INDICATOR CALCULATIONS
# ===============================
s1 = supertrend1(data.High, data.Low, data.Close, 10)
s2 = supertrend2(data.High, data.Low, data.Close, 10)
e1 = ema(data.Close, 10)
print(s1)  # Print Supertrend direction values
print(s2)  # Print Supertrend line values
print(e1)  # Print EMA values


# ===============================
# RUN BACKTEST
# ===============================
bt = Backtest(
    data,
    supertrend_ema,            # Strategy class
    cash=100_000,              # Starting capital
    trade_on_close=True,       # Execute trades on the same bar's close price
    finalize_trades=True       # Close open trades at the end of the backtest
)

# Run the backtest and print performance stats
output = bt.run()
print(output)

# Save trade-by-trade history to CSV for further analysis
print(output['_trades'].to_csv('trades.csv'))

# Uncomment to visualize trades and equity curve on price chart
# bt.plot()


# ===============================
# PARAMETER OPTIMIZATION
# ===============================
def custom_optimization(stats):
    """
    Custom metric for optimization:
    Multiply Total Return (%) by Win Rate (%)
    This rewards strategies with high returns AND high win rates.
    """
    return stats['Return [%]'] * stats['Win Rate [%]']

# Optimize over a range of parameters for best performance
stats = bt.optimize(
    super_length=range(5, 60, 6),  # Try Supertrend ATR length from 5 to 55
    ema_length=range(5, 60, 6),    # Try EMA period from 5 to 55
    maximize=custom_optimization,  # Use custom optimization metric
    max_tries=100,                 # Limit the number of parameter combinations tested
    random_state=42                # Ensure reproducibility
)

# Print optimization results and best strategy configuration
print(stats)
print(stats['_strategy'])

# Plot final strategy performance with best parameters
bt.plot()

# Example best parameters found: Supertrend length = 26, EMA length = 41
# (Will vary depending on data used)
