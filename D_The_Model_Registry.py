def fun(name,layer,lr=0.01):
    print(f"Model: {name}, Layers: {layer}, LR: {lr}")
    
t=int(input())
while t:
    full=input().split()
    a=int(full[0])
    if a==1:
        b,c=full[1],int(full[2])
        fun(b,c)
    elif a==2:
        b,c=full[1],int(full[2])
        fun(layer=c,name=b)
    else:
        b,c,d=full[1],int(full[2]),float(full[3])
        fun(b,c,d)
    
    t-=1