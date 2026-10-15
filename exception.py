lst=[int(i) for i in input().split()]

n=int(input())
try:
    idx=lst[n]
except Exception as e:
    print(e)
else:
    print(idx)