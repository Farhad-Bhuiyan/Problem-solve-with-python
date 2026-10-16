with open('/content/sample_data/data.txt','r') as f:
  string=f.read()
  lst=string.split()
  ans=""
  ln=0
  for i in lst:
    if len(i)>ln:
      ans=i
      ln=len(i)

print(ans)