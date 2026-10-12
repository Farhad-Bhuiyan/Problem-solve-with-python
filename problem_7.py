n=int(input())
lst=[int(x) for x in input().split()]
po,ne,ev,od=0,0,0,0

for i in lst:
    if i>0:
        po+=1
    if i<0:
        ne+=1
    if i&1:
        od+=1
    else:
        ev+=1

print("Positive:",po)
print("Negative:",ne)
print("Even:",ev)
print("Odd:",od)