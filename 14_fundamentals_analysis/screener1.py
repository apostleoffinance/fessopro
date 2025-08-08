from finvizfinance.screener.overview import Overview
foverview = Overview()
filters_dict = {'Exchange':'AMEX','Sector':'Basic Materials', 'P/E': 'Under 15', 'RSI (14)': 'Overbought (80)'}
foverview.set_filter(filters_dict=filters_dict)
df = foverview.screener_view()
print(df)