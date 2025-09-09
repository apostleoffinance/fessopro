#backtrader diff charting is not good 
#vectorbt (liitation) (paid library good) (difficult)

#backtesting py
#good things -easy, good charting, 




#backtrader diff charting is not good
#vectorbt (limitation) (paid library good) (difficult)
#backtesting py 
#good things -easy,good charting ,free,beginner friendly




#fech data

import yfinance as yf
import pandas_ta as ta
from backtesting import Backtest,Strategy
data=yf.download('ETH-USD',start='2025-01-01',end='2025-08-20',interval='1h',multi_level_index=False)
print(data)


def get_sma(close_price,lengtht):
    sma=ta.sma(close_price,lengtht)
    return sma

class sma_strategy(Strategy):
    s1=30
    s2=60
    def init(self):
        self.sma1=self.I(get_sma,self.data.df.Close,self.s1)
        self.sma2=self.I(get_sma,self.data.df.Close,self.s2)

    def next(self):
        if self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            if self.position.is_short:
                self.position.close()
            self.buy()
        elif self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            if self.position.is_long:
                self.position.close()
            self.sell()

bt=Backtest(data,sma_strategy,cash=1000_000,commission=0.01,finalize_trades=True)
result=bt.run()
bt.plot()
print(result)

result['_trades'].to_csv('trades.csv')



output=bt.optimize(s1=range(5,50,2),s2=range(60,120,2),maximize='Return [%]')
print(output)
print(output['_strategy'])
bt.plot()









































# from backtesting import Backtest, Strategy
# from backtesting.lib import crossover

# from backtesting.test import SMA, GOOG


# class SmaCross(Strategy):
#     n1 = 10
#     n2 = 20

#     def init(self):
#         close = self.data.Close
#         self.sma1 = self.I(SMA, close, self.n1)
#         self.sma2 = self.I(SMA, close, self.n2)

#     def next(self):
#         if crossover(self.sma1, self.sma2):
#             self.position.close()
#             self.buy()
#         elif crossover(self.sma2, self.sma1):
#             self.position.close()
#             self.sell()


# bt = Backtest(GOOG, SmaCross,
#               cash=10000, commission=.002,
#               exclusive_orders=True)

# output = bt.run()
# bt.plot()