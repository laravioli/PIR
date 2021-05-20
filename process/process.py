import numpy as np
import pandas as pd

from pathlib import Path

df = pd.DataFrame(pd.read_pickle(Path("data/dataframe.pkl")))
# columns: ['title', 'particule', 'unit', 'time', 'L', 'value']

df = df.loc[(df["title"] == "Ch020") | (df["title"] == "Ch022")]
# selecting data sources of interest

df = df.loc[df["value"] != -1]
# removing "-1" value

starting_time = df.loc[df["title"] == "Ch022"]["time"].min()
df = df.loc[df["time"] >= starting_time]
# selecting time period of interest

# interpolate time
time = df.loc[df["title"] == "Ch020"]["time"].values
time2 = df.loc[df["title"] == "Ch022"]["time"].values

L = sorted(set(df["L"].values))
print(df.loc[(df["L"] == L[10]) & (df["title"] == "Ch020")])
print(df.loc[(df["L"] == L[10]) & (df["title"] == "Ch022")])
