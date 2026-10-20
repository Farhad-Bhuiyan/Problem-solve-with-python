n=int(input())
lst=[0,1]
if n<=2:
    print(lst[n-1])
else:
    cnt=2
    id=1
    while cnt!=n:
        lst.append(lst[-1]+lst[-2])
        cnt+=1
    print(lst[n-1])