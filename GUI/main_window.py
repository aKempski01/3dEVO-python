import tkinter
import customtkinter as ctk


import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)


class Mainwindow():
    root: ctk.CTk
    time: ctk.IntVar
    slider: ctk.CTkSlider
    matrix: np.ndarray


    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("600x600")
        self.time = ctk.IntVar(value=0)



    def __plot(self):
        fig, ax = plt.subplots()
        fig.set_size_inches(4, 4)
        ax.imshow(self.matrix[int(self.slider.get())][:,:,0])

        canvas = FigureCanvasTkAgg(fig, master = self.root)
        canvas.draw()

        canvas.get_tk_widget().place(relx=0.15, rely=0.15)



    def display_output_matrix(self, matrix):
        self.matrix = matrix

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
