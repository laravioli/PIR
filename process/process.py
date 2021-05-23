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


#     L_test = 5

# df_test_1 = pd.DataFrame(resample_time(df_Ch001, df_Ch022)).copy()
# df_x_1 = df_Ch001[df_Ch001.index > df_Ch022.index[0]].copy()
# df_test_1[df_test_1 <= 0] = 0.01
# df_x_1[df_x_1 <= 0] = 0.01
# df_test_1 = df_test_1.apply(lambda x: np.log(x))
# df_x_1 = df_x_1.apply(lambda x: np.log(x))
# df_test_1 = df_test_1.apply(lambda x: (x - x.mean()) / x.std())
# df_x_1 = df_x_1.apply(lambda x: (x - x.mean()) / x.std())

# plt.figure(1)
# plt.plot(df_x_1.index, df_x_1.iloc[:, L_test])
# plt.plot(df_test_1.index, df_test_1.iloc[:, L_test], color="red")
# plt.title("resample then normalise")


# df_x_2 = df_Ch001[df_Ch001.index > df_Ch022.index[0]].copy()
# df_x_2[df_x_2 <= 0] = 0.01
# df_x_2 = df_x_2.apply(lambda x: np.log(x))
# df_x_2 = df_x_2.apply(lambda x: (x - x.mean()) / x.std())

# df_test_2 = pd.DataFrame(resample_time(df_x_2, df_Ch022)).copy()

# plt.figure(2)
# plt.plot(df_x_2.index, df_x_2.iloc[:, L_test])
# plt.plot(df_test_2.index, df_test_2.iloc[:, L_test], color="red")
# plt.title("normalise then resample")
# plt.show()
