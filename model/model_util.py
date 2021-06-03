import numpy as np
import pandas as pd
import torch

from math import floor


def data_scale(df, scaler, log_scale=False, output=False):

    if log_scale:
        df = df.apply(lambda x: x.clip(lower=x[x > 0].min()) if x.min() <= 0 else x)
        df = df.apply(lambda x: np.log10(x))

    scaler = scaler
    scaler.fit(df)
    df_scaled = pd.DataFrame(scaler.transform(df), index=df.index, columns=df.columns)

    if output:
        return df_scaled, scaler
    else:
        return df_scaled


def CNN_data_target_scaled(df_input, df_output, scaler, LOG_SCALE=False):

    df_input_scaled = []

    for df in df_input:
        df_input_scaled.append(data_scale(df, scaler, LOG_SCALE))

    df_output_scaled, output_scaler = data_scale(
        df_output, scaler, LOG_SCALE, output=True
    )

    data_scaled = np.dstack(df_input_scaled)
    data_scaled = np.expand_dims(data_scaled, axis=1)
    data_scaled = torch.tensor(data_scaled, dtype=torch.float)

    target_scaled = df_output_scaled.copy().values
    target_scaled = torch.tensor(target_scaled, dtype=torch.float)

    return data_scaled, target_scaled, output_scaler

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
