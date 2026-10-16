def compute_ratio(x, y):
  try:
    div=(x+y)/(x*y)
  except Exception as e:
    return "Error: Division not possible"
  else:
    return div

x,y=map(int,input().split())
print(compute_ratio(x,y))