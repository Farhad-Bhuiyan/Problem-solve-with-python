n=int(input())
lst=[int(i) for i in input().split()]
lst2=[]
for i in lst:
    if i%2==0:
        lst2.append(i**2)
print(lst2)