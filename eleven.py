li=[]
n=int(input())
for i in range(n):
    x=int(input())
    li.append(x)
positive=0
negative=0
zero=0
for i in li:
    if i>0:
        positive+=1
    elif i<0:
        negative+=1
    else:
        zero+=1
        
print("Positive = ",positive)
print("Negative = ",negative)
print("Zero = ",zero)