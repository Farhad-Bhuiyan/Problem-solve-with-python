n=int(input())
lst=[int(i)for i in input().split()]
rev=lst[::-1]
if lst==rev:
    print("YES")
else:
    print("NO")