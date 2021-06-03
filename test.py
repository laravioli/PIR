import numpy as np
from sklearn.metrics import *


y_true = np.array([[0.5, 1], [-1, 2], [7, -6]])
y_pred = np.array([[0, 2], [-1, 2], [8, -5]])

print(y_true.shape)

print(mean_absolute_percentage_error(y_true, y_pred))
print(mean_squared_error(y_true, y_pred, multioutput="raw_values"))
a = 0
for i in range(len(y_true)):
    a += ((y_pred[i] - y_true[i]) ** 2).mean()
a = a / len(y_true)
print(a)

c = [[1, 2, 3]]
d = [[2, 3, 4]]
print(mean_squared_error(c, d))
