def printer(name,roll,dept):
    print(f"{name} | Roll: {roll} | Dept: {dept}")

n1,r1,d1=input().split()
n2,r2,d2=input().split()

printer(n1,r1,d1)
printer(n2,r2,d2)