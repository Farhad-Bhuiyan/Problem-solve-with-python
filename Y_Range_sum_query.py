n,q=map(int,input().split())
lst=[int(i)for i in input().split()]
sum=[]
sum.append(lst[0])
for i in range(1,n):
    sum.append(sum[i-1]+lst[i])
while q:
    l,r=map(int,input().split())
    if l==1:
        print(sum[r-1])
    else:
        print(sum[r-1]-sum[l-2])
    q-=1
    