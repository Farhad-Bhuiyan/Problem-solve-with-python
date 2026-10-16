lst=[int(i) for i in input().split()]
ans=[]
for i in lst:
  if i%4==0 and i%8!=0:
    ans.append(i)

print(ans)