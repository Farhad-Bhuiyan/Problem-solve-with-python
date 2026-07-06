n=int(input())
sm=1000000
for i in range(n):
    x=int(input())
    if sm > x:
        sm=x
    
print("Small Number: ",sm)