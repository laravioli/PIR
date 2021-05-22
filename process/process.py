import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from utils import *
from pathlib import Path

df_Ch001 = pd.DataFrame(pd.read_pickle(Path("data/Ch001.pkl")))
df_Ch009 = pd.DataFrame(pd.read_pickle(Path("data/Ch009.pkl")))
df_Ch020 = pd.DataFrame(pd.read_pickle(Path("data/Ch020.pkl")))
df_Ch022 = pd.DataFrame(pd.read_pickle(Path("data/Ch022.pkl")))

dfs = [df_Ch001, df_Ch009, df_Ch020]

L_test = 15

df_test_1 = pd.DataFrame(resample_time(df_Ch020, df_Ch022)).copy()
df_x_1 = df_Ch020[df_Ch020.index > df_Ch022.index[0]].copy()
df_test_1[df_test_1 <= 0] = 0.01
df_x_1[df_x_1 <= 0] = 0.01
df_test_1 = df_test_1.apply(lambda x: np.log(x))
df_x_1 = df_x_1.apply(lambda x: np.log(x))
df_test_1 = df_test_1.apply(lambda x: (x - x.mean()) / x.std())
df_x_1 = df_x_1.apply(lambda x: (x - x.mean()) / x.std())

plt.figure(1)
plt.plot(df_x_1.index, df_x_1.iloc[:, L_test])
plt.plot(df_test_1.index, df_test_1.iloc[:, L_test], color="red")
plt.title("resample then normalise")


df_x_2 = df_Ch020[df_Ch020.index > df_Ch022.index[0]].copy()
df_x_2[df_x_2 <= 0] = 0.01
df_x_2 = df_x_2.apply(lambda x: np.log(x))
df_x_2 = df_x_2.apply(lambda x: (x - x.mean()) / x.std())

df_test_2 = pd.DataFrame(resample_time(df_x_2, df_Ch022)).copy()

plt.figure(2)
plt.plot(df_x_2.index, df_x_2.iloc[:, L_test])
plt.plot(df_test_2.index, df_test_2.iloc[:, L_test], color="red")
plt.title("normalise then resample")
plt.show()
