s=input()
ans=[]
x=""
l,r=0,0
for c in s:
    x+=c
    if c=='L':
        l+=1
    if c=='R':
        r+=1
    if l==r:
        ans.append(x)
        x=""

print(len(ans))
for st in ans:
    print(st)