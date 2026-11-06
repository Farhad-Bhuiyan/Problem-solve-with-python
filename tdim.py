import numpy as np

ar1=np.array([10,20.30,40])

print(ar1.ndim)
print(ar1.shape)

ar2=np.array([[10,20,30],
              [40,50,60]])
print(ar2.ndim)
print(ar2.shape)

ar3=np.array([
    [[10,20,30],
     [40,50,60]],
    [[10,20,30],
    [40,50,60]]
])

print(ar3.ndim)
print(ar3.shape)