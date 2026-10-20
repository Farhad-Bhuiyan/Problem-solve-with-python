n=int(input())
lst=[int(i) for i in input().split()]

cnt={}
for i in lst:
    if i in cnt:
        cnt[i]+=1
    else:
        cnt[i]=1

ans=0;
for i in cnt:
    if cnt[i]>=i:
        ans+=cnt[i]-i
    else:
        ans+=cnt[i]
print(ans)