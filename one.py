n=int(input())
od=0
ev=0
for i in range(n):
    x=int(input())
    if(i&1):
        od+=i
    else:
        ev+=i
print("Odd sum = ",od)
print("Even sum = ",ev)