n=int(input())
if n<=1:
    print(f"{n} is not a prime number")
else:
    flag=True
    for i in range(2,n):
        if n%i==0:
            flag=False
            break
    if flag:
        print(f"{n} is a prime number")
    else:
        print(f"{n} is not a prime number")