import numpy as np
import pandas as pd
import torch

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from math import floor


def data_log_scaler(df, log_noise=1, scaler=MinMaxScaler(), output=False):

    # log transformation
    log_noise = 1 if log_noise <= 0 else log_noise
    noise = lambda x: x.clip(lower=x[x > 0].min() * log_noise) if x.min() <= 0 else x
    df = df.apply(noise)
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


def data_formatter(data_input, data_target, network, window=1):

    if network == "mlp":
        data_input = np.concatenate(data_input, axis=1)

    elif network == "cnn_v1":
        data_input = np.dstack(data_input)
        data_input = np.expand_dims(data_input, axis=1)

    elif network == "cnn_v2":
        for i, data in enumerate(data_input):
            list = np.split(data, len(data) / window)
            data_input[i] = np.array(list)
        data_input = np.stack(data_input, axis=1)

        list = np.split(data_target, len(data_target) / window)
        data_target = np.array(list)

    return data_input, data_target


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


def CNN_v2_scale_format(
    df_input, df_target, log_noise=1, scaler=MinMaxScaler(), window=40
):

    len = 4720
    data_input_scaled = []

    # scale and format input
    for i, df in enumerate(df_input):
        data_input_scaled.append(data_scale(df, scaler=scaler))
        data_input_scaled[i] = np.array(
            np.split(data_input_scaled[i][:len], len / window)
        )

    data_scaled = np.stack(data_input_scaled, axis=1)
    data_scaled = torch.tensor(data_scaled, dtype=torch.float)

    # scale and format output
    target_scaled, output_scaler = data_scale(
        df_target, log_noise=log_noise, scaler=scaler, output=True
    )
    target_scaled = np.array(np.split(target_scaled[:len], len / window))
    target_scaled = torch.tensor(target_scaled, dtype=torch.float)

    return data_scaled, target_scaled, output_scaler


def data_splitter(df_input, df_output, window):
    if nn_type == "cnn_v2":
        split = int(4720 / window * 0.15)
    else:
        split = int(len(df.index) * 0.15)
    return split

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
