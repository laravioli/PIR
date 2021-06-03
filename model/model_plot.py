import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from matplotlib.colors import LogNorm

df_Ch022 = pd.DataFrame(
    pd.read_pickle(Path("C:/Users/Victor/Desktop/PIR/process/Ch022.pkl"))
)
df_data_pred = pd.DataFrame(
    pd.read_pickle(
        Path("C:/Users/Victor/Desktop/PIR/model/saved_models/SVM_predictions.pkl")
    )
)
df_data_metrics = pd.DataFrame(
    pd.read_pickle(
        Path("C:/Users/Victor/Desktop/PIR/model/saved_models/SVM_metrics.pkl")
    )
)

df_data_pred = df_data_pred.iloc[:, :-1]
df_data_metrics = df_data_metrics.iloc[:-1]

plt.figure(figsize=(20, 10))
plt.pcolormesh(
    df_Ch022.index,
    df_Ch022.columns,
    df_Ch022.values.T / df_data_pred.values.T,
    norm=LogNorm(1e-1, 10),
    shading="auto",
)
plt.colorbar()
plt.show()

print(df_data_metrics)

plt.figure()
plt.plot(df_Ch022.columns[3:], df_data_metrics.iloc[3:, 0])

plt.show()
