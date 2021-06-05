import numpy as np
import pandas as pd
import torch

from sklearn.preprocessing import MinMaxScaler
from math import floor


def data_scale(df, log_noise=1, scaler=MinMaxScaler(), output=False):
    # log scaling
    if log_noise <= 0:
        log_noise = 1
    df = df.apply(
        lambda x: x.clip(lower=x[x > 0].min() * log_noise) if x.min() <= 0 else x
    )
    df = df.apply(lambda x: np.log10(x))

    # sklearn scaling
    scaler = scaler
    scaler.fit(df)
    data_scaled = scaler.transform(df)
    # return a numpy array with scaled data
    if output:
        return data_scaled, scaler
    else:
        return data_scaled


def CNN_scale_format(df_input, df_target, log_noise=1, scaler=MinMaxScaler()):

    data_input_scaled = []

    # scale and format input
    for df in df_input:
        data_input_scaled.append(data_scale(df, scaler=scaler))

    data_scaled = np.dstack(data_input_scaled)
    data_scaled = np.expand_dims(data_scaled, axis=1)
    data_scaled = torch.tensor(data_scaled, dtype=torch.float)

    # scale and format output
    target_scaled, output_scaler = data_scale(
        df_target, log_noise=log_noise, scaler=scaler, output=True
    )
    target_scaled = torch.tensor(target_scaled, dtype=torch.float)

    return data_scaled, target_scaled, output_scaler


def FNN_scale_format(df_input, df_target, log_noise=1, scaler=MinMaxScaler()):

    # scale and format input
    data_input = pd.concat(df_input, axis=1)
    input_scaled = data_scale(data_input, scaler=scaler)
    input_scaled = torch.tensor(input_scaled, dtype=torch.float)

    # scale and format target
    target_scaled, output_scaler = data_scale(
        df_target, log_noise=log_noise, scaler=scaler, output=True
    )
    target_scaled = torch.tensor(target_scaled, dtype=torch.float)

    return input_scaled, target_scaled, output_scaler

    """
Utility function for computing output of convolutions
takes a tuple of (h,w) and returns a tuple of (h,w)
"""


def num2tuple(num):
    return num if isinstance(num, tuple) else (num, num)


def conv_output_shape(h_w, kernel_size=1, stride=1, pad=0, dilation=1):
    kernel_size, stride, pad, dilation = (
        num2tuple(kernel_size),
        num2tuple(stride),
        num2tuple(pad),
        num2tuple(dilation),
    )
    pad = num2tuple(pad[0]), num2tuple(pad[1])

    h = floor(
        (h_w[0] + sum(pad[0]) - dilation[0] * (kernel_size[0] - 1) - 1) / stride[0] + 1
    )
    w = floor(
        (h_w[1] + sum(pad[1]) - dilation[1] * (kernel_size[1] - 1) - 1) / stride[1] + 1
    )

    return h, w
