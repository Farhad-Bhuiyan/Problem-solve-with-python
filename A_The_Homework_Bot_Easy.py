def check_pass(marks):
    return marks>=40

n=int(input())
if check_pass(n):
    print("Pass")
else:
    print("Fail")
