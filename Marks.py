t=int(input())
while t:
    marks=int(input())
    if marks>=80:
        print("A+")
    elif marks>=70:
        print("A")
    elif marks>=40:
        print("Pass")
    else:
        print("Fail")
    
    t-=1