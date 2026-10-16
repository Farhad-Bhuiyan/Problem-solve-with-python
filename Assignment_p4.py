str=input()
lst=str.split()
ans=[]
for i in lst:
  if i[0]=='A' or i[0]=='a' or i[0]=='E' or i[0]=='e' or i[0]=='I' or i[0]=='i'or i[0]=='O' or i[0]=='o' or i[0]=='U' or i[0]=='u':
    ans.append(i)

print(ans)