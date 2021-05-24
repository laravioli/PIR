import numpy as np

a = [1, 2, 3, 4, 5, 6]
b = [7, 8, 9, 10, 11, 12]

c = np.dstack((a, b))
print(c)
print(c.mean(axis=2))
