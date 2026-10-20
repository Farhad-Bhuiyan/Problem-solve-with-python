n=int(input())
lst=[int(i) for i in input().split()]

ans=10**100
for i in lst:
    cnt=0
    v=i
    while v%2==0:
        cnt+=1
        v/=2
    ans=min(ans,cnt)
    
print(ans)