import datetime as Dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def fyear2datetime(year):

    iyear = int(year)
    y = Dt.datetime(iyear, 1, 1)
    yn = Dt.datetime(iyear + 1, 1, 1)
    dt = yn - y
    return y + (year - iyear) * dt


def style_diff(df, df_orig):

    style = {True: "", False: "color: red; background-color: yellow"}
    df_style = (df == df_orig).replace(style)
    return df.style.apply(lambda x: df_style, axis=None)


def format_data(df, df_ref):

    df = df[df.index > df_ref.index[0]].copy()
    df[df <= 0] = 0.01
    df = df.apply(lambda x: np.log(x))
    df = df.apply(lambda x: (x - x.mean()) / x.std())

    return df


def resample_time(df1, df_ref):

    df2 = pd.DataFrame(index=df_ref.index, columns=df1.columns)
    df3 = pd.concat([df1, df2], copy=True)
    df3 = df3.sort_index(axis=0).interpolate(method="linear").dropna()
    df3 = df3[df3.index.isin(df_ref.index)]

    return df3


def plot_processing(df, df1, df2, L):

    plt.figure(1)
    plt.plot(df.index, df.iloc[:, L])
    plt.plot(df1.index, df1.iloc[:, L], color="red")
    plt.title("resample then normalise")

    plt.figure(2)
    plt.plot(df.index, df.iloc[:, L])
    plt.plot(df2.index, df2.iloc[:, L], color="red")
    plt.title("normalise then resample")
    plt.show()
