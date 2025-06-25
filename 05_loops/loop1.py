#iterable
l1=[44,55,66,77]

#print(45 in l1)

#type 1 loop
total = 0 # 44 -> 99 -> 165 -> 242
for i in l1:
    total=total+i # 0+44 -> 44+55 -> 99+66 -> 165+77

print(total) # 44 -> 99 -> 165 -> 242

# Average
num=len(l1)
print(num)
average = total/num
print("Avg is" , average)

#type 2 loop - It is used to run a piece of code for n number of times | Generating the lists
print(list(range(20))) #Range function is a function that generates a list of n numbers

for i in range(10):
    print('hello', i)

l1 =[]
for i in range(100):
    if i%2 == 0:
        l1.append(i)
        #print(i)
print(l1)

