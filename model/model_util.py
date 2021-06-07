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
    else:
        print("carefull, u must have misswritten network name")

    return data_input, data_target


def formatting_data_2(data_input):
    size = 4720
    data_input = np.stack(data_input, axis=1)

    data = list()
    n1, n2 = 0, 118
    data.append(data_input[n1:n2])
    while n2 < size:
        n1 += 59
        n2 += 59
        data.append(data_input[n1:n2])

    a = np.array(data)
    a = np.swapaxes(a, 1, 2)
    return a

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
