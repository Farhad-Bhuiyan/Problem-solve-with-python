n=int(input())

lst=[]
while n:
    lst.append(n%10)
    n//=10
    
for i in lst:
    print(i,end=' ')
    