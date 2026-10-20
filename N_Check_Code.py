a,b=map(int,input().split())
st=input()
if st[a]=='-':
    for i in range(0,a+b+1):
        if i!=a and st[i].isdigit()==False:
            print("No")
            break
    else:
        print("Yes")
else:
    print("No")