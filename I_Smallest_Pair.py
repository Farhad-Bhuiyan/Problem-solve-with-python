t=int(input())
while t:
    n=int(input())
    mn=10**100
    lst=[int(i) for i in input().split()]
    for i in range(0,n-1):
        for j in range(i+1,n):
            if (lst[i]+lst[j]+((j+1)-(i+1)))<mn:
                mn=lst[i]+lst[j]+((j+1)-(i+1))
    
    print(mn)
    t-=1