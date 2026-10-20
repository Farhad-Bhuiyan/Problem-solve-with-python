a,b=map(int,input().split())
ans=[]
for i in range(a,b+1,1):
    st=str(i)
    for c in st:
        if c!='4' and c!='7':
            break;
    else:
        ans.append(st)
        
if ans:
    print(*ans)
else:
    print(-1)