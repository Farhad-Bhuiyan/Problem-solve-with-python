n=int(input())
lst=[int(i) for i in input().split()]
c=0
for i in lst:
    if i%2==0:
        continue
    
    sum=0
    nm=i
    while i:
        sum+=i%10
        i//=10        
    if sum>20:
        break
    else:
        print(nm,sum)
        c+=1

print(c)