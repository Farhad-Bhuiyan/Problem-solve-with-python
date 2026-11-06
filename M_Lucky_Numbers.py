a,b=map(int,input().split())
ans=[]
for i in range(a,b+1,1):
    st=str(i)
    if all(d in '47' for d in st):
        ans.append(st)
        
if ans:
    print(*ans)
else:
    print(-1)