str=input()
dec={}
for i in str:
    dec[i]=dec.get(i,0)+1
    
for k in sorted(dec.keys()):
    print(f"{k} : {dec[k]}")