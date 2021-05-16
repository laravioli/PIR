from onemap import read
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

def plot_test():
    for i in range(4):
        data, meta = read("NPOES_DATA/NPOES15_SEM2_PROT_2500keV_200{}.map".format(i))
        plt.figure(i+1)
        plt.pcolormesh(meta['x'], meta['y_mean'], data.T, norm=LogNorm(), shading='auto')
        plt.gca().set_title(meta['title'])
        plt.xlabel(meta['x_title'])
        plt.ylabel(meta['y_title'])

    plt.show()

plot_test()