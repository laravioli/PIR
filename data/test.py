import matplotlib.pyplot as plt
from utils import *

from pathlib import Path

plot_map(
    Path(
        "C:/Users/Victor/Desktop/PIR/data/NPOES_DATA/Ch009/NPOES14_SEM_ELEC_0100keV_1999.map"
    )
)

values, meta = read(
    "C:/Users/Victor/Desktop/PIR/data/NPOES_DATA/Ch009/NPOES14_SEM_ELEC_0100keV_1999.map"
)
print(meta["y_mean"][15:].shape)
