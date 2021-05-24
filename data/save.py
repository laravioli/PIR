import numpy as np
import pandas as pd

from utils import *


df_map = {}
data_dir = "data/NPOES_DATA/"

for d in os.listdir(data_dir):
    folder = os.path.join(data_dir, d)
    files = []
    files += [os.path.join(folder, f) for f in os.listdir(folder)]
    frames = [map_to_frame(f) for f in files]
    df = pd.concat(frames)
    df.name = d
    df_map[d] = df

for name, df in df_map.items():

    df.to_pickle(Path(f"data/{name}.pkl"))
