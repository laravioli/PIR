import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch
import pandas as pd
from torch import nn, optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from ignite.engine import Events, create_supervised_trainer, create_supervised_evaluator
from ignite.metrics import Accuracy, Loss, RunningAverage, ConfusionMatrix
from ignite.handlers import ModelCheckpoint, EarlyStopping

from pathlib import Path


df_Ch001 = pd.DataFrame(pd.read_pickle(Path("process/Ch001.pkl")))
df_Ch009 = pd.DataFrame(pd.read_pickle(Path("process/Ch009.pkl")))
df_Ch020 = pd.DataFrame(pd.read_pickle(Path("process/Ch020.pkl")))
df_Ch022 = pd.DataFrame(pd.read_pickle(Path("process/Ch022.pkl")))

df = np.dstack((df_Ch001.values, df_Ch009.values, df_Ch020.values))


# import torch.utils.data as data_utils

# # Creating np arrays
# target = df['Target'].values
# features = df.drop('Target', axis=1).values

# # Passing to DataLoader
# train = data_utils.TensorDataset(features, target)
# train_loader = data_utils.DataLoader(train, batch_size=10, shuffle=True)

# import pandas as pd
# import numpy as np
# import torch

# df = pd.read_csv('train.csv')
# target = pd.DataFrame(df['target'])
# del df['target']
# train = data_utils.TensorDataset(torch.Tensor(np.array(df)), torch.Tensor(np.array(target)))
# train_loader = data_utils.DataLoader(train, batch_size = 10, shuffle = True)

# import pandas as pd
# import torch

# # determine the supported device
# def get_device():
#     if torch.cuda.is_available():
#         device = torch.device('cuda:0')
#     else:
#         device = torch.device('cpu') # don't have GPU
#     return device

# # convert a df to tensor to be used in pytorch
# def df_to_tensor(df):
#     device = get_device()
#     return torch.from_numpy(df.values).float().to(device)

# df_tensor = df_to_tensor(df)
# series_tensor = df_to_tensor(series)
