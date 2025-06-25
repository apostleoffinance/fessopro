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