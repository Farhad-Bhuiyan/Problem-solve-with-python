sum = 0
lst=[int(i) for i in input().split()]
for i in lst:
    if i<0:
        break
    sum+=i
print(sum)