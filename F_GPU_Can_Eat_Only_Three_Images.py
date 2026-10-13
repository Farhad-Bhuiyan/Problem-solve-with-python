def bm(lst,bs):
    for i in range(0,len(lst),bs):
        yield lst[i:i+bs]

def mean(batch):
    return sum(batch)/len(batch)

n,bs=map(int,input().split())
lst=[int(i) for i in input().split()]
for batch in bm(lst,bs):
    print(f"{batch} mean={mean(batch)}")