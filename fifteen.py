def check(a):
    if a&1:
        print(f"{a} is odd")
    else:
        print(f"{a} is even")

a=int(input())
check(a)