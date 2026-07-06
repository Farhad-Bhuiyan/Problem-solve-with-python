li=[]
n=int(input())
for i in range(n):
    x=int(input())
    li.append(x)

max=0
for i in li:
    if i>max:
        max=i
print("Maximum = ",max)