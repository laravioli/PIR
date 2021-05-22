import datetime as Dt
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


def resample_time(df, df_ref):

    t_0 = df_ref.index[0]
    df = df[df.index > t_0]
    df2 = pd.DataFrame(index=df_ref.index, columns=df.columns)
    df3 = pd.concat([df, df2])
    df3 = df3.sort_index(axis=0).interpolate(method="linear").dropna()
    df3 = df3[df3.index.isin(df_ref.index)]

    return df3
