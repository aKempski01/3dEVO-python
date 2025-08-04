from matplotlib import pyplot as plt
import os
import glob

def save_plt(figure: plt.Figure, filename: str, plot_name: str) -> None:

    path = filename + "/plots"

    if not os.path.exists(path):
        os.makedirs(path)

    if os.path.exists(path + "/" + plot_name + ".png"):
        plot_name = plot_name + "_" + str(len(glob.glob(path + "/" + plot_name + "*.png")))

    figure.savefig(path + "/" + plot_name + ".png")


