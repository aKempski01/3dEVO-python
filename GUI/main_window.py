import itertools
import tkinter
import customtkinter as ctk

import plotly.express as px
import pandas as pd

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

import config


class Mainwindow():
    root: ctk.CTk
    time: ctk.IntVar
    slider: ctk.CTkSlider
    matrix: np.ndarray
    fitness: list

    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1000x1000")
        self.time = ctk.IntVar(value=0)

        # self.figs = []
        # self.axs = []

        self.fig, self.axs = plt.subplots(figsize=(8, 3), ncols=config.num_of_phenotypes)
        self.fig_3d = plt.figure(figsize=(8, 6), dpi=100)
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        self.fig_los = plt.figure()
        self.ax_los = self.fig_los.add_subplot(111)


        # self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=self.root)
        # canvas_widget = self.canvas_3d.get_tk_widget()
        # canvas_widget.pack(fill=ctk.BOTH, expand=True)

        # for p in range(config.num_of_phenotypes):
        #     fig, ax = plt.subplots()
        #     fig.set_size_inches(4, 4)
        #     ax.title.set_text("Phenotype {}".format(p))
        #     self.figs.append(fig)
        #     self.axs.append(ax)

    def __plot_2d(self):
        for p in range(config.num_of_phenotypes):
            self.axs[p].imshow(self.matrix[int(self.slider.get())][:, :, p],cmap='gray')

        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.05, rely=0.15)
        self.__plot_loss_history()

    def __plot_3d(self):
        self.ax_3d.clear()
        m = self.matrix[int(self.slider.get())]

        idx = list(itertools.product(range(config.pop_length), range(config.pop_length), range(config.pop_length)))

        c = []
        for i in idx:
            c.append(m[i[0], i[1], i[2], 0])


        df = pd.DataFrame(idx, columns=['x', 'y', 'z'])
        df['color'] = c
        # m = np.argwhere(m[:, :, :, 0] == 1)

        self.ax_3d.scatter(df['x'],df['y'], df['z'], c=df['color'])

        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=self.root)
        self.canvas_3d.draw()
        self.canvas_3d.get_tk_widget().place(relx=0.05, rely=0.15)
        # canvas_widget = self.canvas_3d.get_tk_widget()
        # canvas_widget.pack(fill=ctk.BOTH, expand=True)





    def __plot(self):
        if config.num_of_dims == 2:
            self.__plot_2d()
        elif config.num_of_dims == 3:
            self.__plot_3d()





    def __plot_loss_history(self):
        self.ax_los.plot(self.fitness)

        canvas = FigureCanvasTkAgg(self.fig_los, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.05, rely=0.45)



    def display_output_matrix(self, matrix, fitness):
        self.matrix = matrix
        self.fitness = fitness

        self.root.update()

        plot_button = ctk.CTkButton(master=self.root,
                             command=self.__plot,
                             height=2,
                             width=10,
                             text="Plot")

        self.slider = ctk.CTkSlider(self.root,
                   variable=self.time,
                   from_=0,
                   to=len(self.matrix)-1)

        plot_button.pack()
        self.slider.pack()

        self.root.mainloop()
