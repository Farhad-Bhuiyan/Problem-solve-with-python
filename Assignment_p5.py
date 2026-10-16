str=input()
str=str.lower()

l,r=0,len(str)-1
while(l<r):
  if str[l]!=str[r]:
    print("Not Palindrome")
    break
  l+=1
  r-=1
else:
  print("Palindrome")