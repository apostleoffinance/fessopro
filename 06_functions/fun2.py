#local variable
#global variable

name = 'tsla'

def average(numbers:list)->int:
    """
    this function will calc avg value
    """
    print(name)

    total=0
    for i in numbers:
        total=total+i
    avg=total/len(numbers)


    return avg

prices=[1,33,44,55,66]
avg=average(prices)
print(avg)

print(name)