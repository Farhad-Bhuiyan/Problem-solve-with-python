n=int(input())
lst=[int(i) for i in input().split()]
mi,xi=0,0
mx,mn=0,10**100
for i in range(0,n):
    if mx<lst[i]:
        mx=lst[i]
        xi=i
    if mn>lst[i]:
        mn=lst[i]
        mi=i

lst[mi],lst[xi]=lst[xi],lst[mi]
print(*lst)