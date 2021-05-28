import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from process import *
from pathlib import Path

df_Ch001 = pd.DataFrame(pd.read_pickle(Path("data/Ch001.pkl")))
df_Ch009 = pd.DataFrame(pd.read_pickle(Path("data/Ch009.pkl")))
df_Ch020 = pd.DataFrame(pd.read_pickle(Path("data/Ch020.pkl")))
df_Ch022 = pd.DataFrame(pd.read_pickle(Path("data/Ch022.pkl")))

dfs = [df_Ch001, df_Ch009, df_Ch020]

df = dfs[0]
L = 30

df1 = resample_time(df, df_Ch022)
df1 = format_data(df1, df_Ch022)

df2 = format_data(df, df_Ch022)
df2 = resample_time(df2, df_Ch022)

plot_processing(format_data(df, df_Ch022), df1, df2, L)
