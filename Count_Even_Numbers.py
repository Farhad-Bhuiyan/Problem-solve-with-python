n=int(input())
count=0
lst=[int(i)for i in input().split()]
for i in lst:
    if i%2==0:
        count+=1

print(count)