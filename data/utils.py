import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from pathlib import Path
from matplotlib.colors import LogNorm

HEADER_SIZE = 8


def read(file):
    """
    Reads a MAP file.

    Parameters
    ----------
    file : str
        Path to the file to read.

    Returns
    -------
    data : array_like
        Array of values from the map file.
    meta : dict
        Metadata from the map file. The following fields are available :

         - ``'header'`` : array of header lines
         - ``'x'`` : Coordinates on the first dimension
         - ``'y'`` : Coordinates on the second dimension (bins)
         - ``'y_mean'`` : Coordinates on the second dimension (mean of bins)
         - ``'title'`` : Title of the map
         - ``'x_title'``, ``'y_title'`` : Title of the axis
         - ``'unit'`` : Unit of the values

    Examples
    --------
    >>> from onemap import read
    >>> import matplotlib.pyplot as plt
    >>> from matplotlib.colors import lognorm
    >>> data, meta = read("fluxDIFF_XXX_.map")
    >>> plt.pcolormesh(meta['x'], meta['y_mean'], data.T, norm=LogNorm())
    >>> plt.gca().set_title(meta['title'])
    >>> plt.xlabel(meta['x_title'])
    >>> plt.ylabel(meta['y_title'])
    """
    with open(file) as f:
        header = []
        for i in range(HEADER_SIZE):
            header.append(f.readline().strip())
        shape_line = f.readline()
        n_x, n_y = re.match(r"\s*(\d+)\s+(\d+)\s*", shape_line).groups((1, 2))
        n_x, n_y = int(n_x), int(n_y)
        x_grid = []
        y_grid = []
        values = np.zeros((n_x, n_y - 1))
        f.readline()
        for i in range(n_y):
            value = f.readline().strip()
            if value:
                y_grid.append(float(value))
        pattern = r"\s+".join([r"(\S+)"] * (n_y))
        re_pr = re.compile(pattern)
        for i in range(n_x):
            value = f.readline().strip()
            match = re_pr.match(value)
            if match is None:
                raise RuntimeError("Could not parse input file '{}'".format(file))
            x_grid.append(float(match.group(1)))
            for j in range(n_y - 1):
                values[i, j] = float(match.group(j + 2))
    y_grid = np.array(y_grid)
    return values, {
        "header": header,
        "title": header[0],
        "x_title": header[6],
        "y_title": header[7],
        "unit": header[4],
        "x": np.array(x_grid),
        "y": y_grid,
        "y_mean": (y_grid[:-1] + y_grid[1:]) / 2,
    }


def map_to_frame(filename):

    filename = Path(filename)
    values, meta = read(filename)

    df = pd.DataFrame(
        data=values[:, 15:-1], index=meta["x"], columns=meta["y_mean"][15:-1]
    )

    return df


def plot_map(filename):

    data, meta = read(filename)
    plt.figure()
    plt.pcolormesh(meta["x"], meta["y_mean"], data.T, norm=LogNorm(), shading="auto")
    plt.gca().set_title(meta["title"])
    plt.xlabel(meta["x_title"])
    plt.ylabel(meta["y_title"])
    plt.show()
