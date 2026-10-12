n=int(input())
lst=[int(x) for x in input().split()]
fl=True
ans=10**100
for i in lst:
    if i>100:
        ans=min(ans,i)

print(ans)    
