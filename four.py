first,second=0,0
n=int(input())
for i in range(n):
    x=int(input())
    if x>first:
        first=x
    if first>x and x>second:
        second=x

print("Maximum = ",first)
print("Second Maximum = ",second)