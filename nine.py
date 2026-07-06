li=[]
n=int(input())
for i in range(n):
    x=int(input())
    li.append(x)

sum=0
for i in li:
    sum+=i
print("Total = ",sum)