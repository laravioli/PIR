from math import floor, ceil
from typing import Tuple
import numpy as np
import pandas as pd


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

    """
Laboratory for CNN shape
"""


# print("conv1 :", conv_output_shape((34, 3), 3, pad=1), 34 * 3 * 50)
# print("maxpool2d :", conv_output_shape((34, 3), (2, 1), stride=(2, 1)), 17 * 3 * 50)
# print("conv2 :", conv_output_shape((17, 3), 3), 15 * 150)
# print("maxpool2d :", conv_output_shape((15, 1), (3, 1), stride=(3, 1)), 5 * 150)
