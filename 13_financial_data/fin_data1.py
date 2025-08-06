#crypto
#forex
#equity
#option
#futures


#pip install yfinance
import yfinance as yf

ticker1 = 'BTC-USD'
# data=yf.download(ticker1, period='5y', multi_level_index=False)
# print(data)

# l1=[]

# for i in data.columns:
#     print(i)
#     l1.append(i[0])
# data.columns = l1


data=yf.download(ticker1, start='2024-01-01', end='2025-07-11', interval='1d', multi_level_index=False,ignore_tz=True)
print(data)