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
