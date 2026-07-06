li=[]
n=int(input())
for i in range(n):
    x=int(input())
    li.append(x)

max=0
min=1000000
for i in li:
    if max<i:
        max=i
    if min>i:
        min=i

print("Differanc = ",max-min)