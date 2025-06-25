#Problem 1

l1=[4,2,6,7,894,45,67]

largest=l1[0]
for i in l1:
    if largest < i:
        largest=i
print(largest) 


#Problem 2
# Calculate VWAP 
prices = [100, 105, 110]
volumes = [200, 150, 300]

num = 0
den = 0

for i in range(len(prices)):
    n=prices[i]*volumes[i]
    num = num+n
    den = den+volumes[i]
    vwap = num/den
    #v = sum(volumes*prices)
    #vwap = v/sum(volumes)

print(vwap)

#Problem 3
# Total Dividend Income
stock_quantities = [100,200,150]
dividends = [0.5,1,0.2]

total_d_income = 0

for i in range(len(stock_quantities)):
    q = stock_quantities[i] * dividends[i]
    total_d_income = total_d_income+q
    #print(total_d_income)
#     q = stock_quantities[i] * dividends[i]
print("Total Dividend Income is " , total_d_income)

#Problem 4
#Profitable Trades Counter

trade_outcome = [20, -10, 15, -5, 30]

profit = 0
for i in trade_outcome:
    if i > 0:
        profit=profit+1
        #profit+=1
print("Number of Profitable Trades are", profit)