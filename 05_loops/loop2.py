stock_prices = {'amzn':500, 'tsla':900, 'goog':780}

for i in stock_prices:
    print(i, stock_prices.get(i))


# Type 4 Loop

print(list(stock_prices.keys()))
print(list(stock_prices.values()))
print(list(stock_prices.items()))

for i in stock_prices.keys():
    print(i)

for i in stock_prices.values():
    print(i)

#type 4
for i in stock_prices.items():
    print(i)

for i,j in stock_prices.items():
    print(i,j)