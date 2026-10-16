lst=[1,2,3,4,5,6]
even=filter(lambda i:i%2==0,lst)
result=list(map(lambda i:i**2,even))
print(result)
