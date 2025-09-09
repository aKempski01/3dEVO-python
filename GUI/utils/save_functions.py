from matplotlib import pyplot as plt
import os
import glob
from pyqttoast import Toast, ToastPreset


def save_plt(figure: plt.Figure, filename: str, plot_name: str) -> str:

    path = filename + "/plots"

    if not os.path.exists(path):
        os.makedirs(path)

    if os.path.exists(path + "/" + plot_name + ".png"):
        plot_name = plot_name + "_" + str(len(glob.glob(path + "/" + plot_name + "*.png")))

    figure.savefig(path + "/" + plot_name + ".png")

    return path + "/" + plot_name + ".png"



def save_common_plot(figure: plt.Figure, plot_name: str):
    path = "common_plots"

    if not os.path.exists(path):
        os.makedirs(path)

    if os.path.exists(path + "/" + plot_name + ".png"):
        plot_name = plot_name + "_" + str(len(glob.glob(path + "/" + plot_name + "*.png")))

    figure.savefig(path + "/" + plot_name + ".png")

    return path + "/" + plot_name + ".png"
