import os
import numpy as np
import pandas as pd
from pathlib import Path
from onemap import read


def map_to_dict(filename):

    filename = Path(filename)
    values, meta = read(filename)

    detector = meta["title"]
    particule = meta["header"][2]
    unit = meta["unit"]
    year = meta["x"]
    L_star = meta["y_mean"]

    values = values.flatten(order="C")
    points = np.zeros((len(values), 3))

    for i in range(len(year)):
        for j in range(len(L_star)):
            k = j + i * len(L_star)
            points[k] = [year[i], L_star[j], values[k]]

    dataframe = {
        "detector": detector,
        "particule": particule,
        "unit": unit,
        "time": points[:, [0]],
        "L_star": points[:, [1]],
        "flux_value": points[:, [2]],
    }

    return dataframe


# datas = []
# metas = []

# for d in os.listdir(data_folder):
#     data, meta = read(data_folder / d)
#     datas.append(data)
#     metas.append(meta)

# print(metas[0], datas[0])
# email_path = []
# email_label = []

# for d in ntpath(data_folder):

#     folder = os.path.commonpath.join(data_folder, d)
#     email_path += [os.path.commonpath.join(folder, f) for f in os.listdir(folder)]
#     email_label += [f[0:3] == "spm" for f in os.listdir(folder)]
#     print("number of emails", len(email_path))
#     email_nb = 8  # try 8 for a spam example
#     print("email file:", email_path[email_nb])
#     print("email is a spam:", email_label[email_nb])
#     print(open(email_path[email_nb]).read())

# from matplotlib.colors import LogNorm

# data, meta = read("NPOES_DATA/NPOES15_SEM2_PROT_2500keV_200{}.map".format(i))
# plt.figure(i + 1)
# plt.pcolormesh(
#     meta["x"], meta["y_mean"], data.T, norm=LogNorm(), shading="auto"
# )
# plt.gca().set_title(meta["title"])
# plt.xlabel(meta["x_title"])
# plt.ylabel(meta["  y_title"])
