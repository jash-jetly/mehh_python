import numpy as np

r = np.random.randint(1, 7, 1000)
c=np.bincount(r)[1:]
p = c / 1000
print(p)



import numpy as np
s_r=np.array([1, 2, np.nan, 4, np.nan])
print(np.isnan(s_r).sum())

