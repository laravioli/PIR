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

dfs_processed = []

for df_Ch in dfs:

    df_Ch.columns = df_Ch022.columns
    df = format_data(df_Ch, df_Ch022)
    df = resample_time(df, df_Ch022)
    dfs_processed.append(df)

dfs_processed.append(format_data(df_Ch022, df_Ch022))

name = ["Ch001", "Ch009", "Ch020", "Ch022"]
for name, df in zip(name, dfs_processed):
    df.to_pickle(Path(f"process/{name}.pkl"))
