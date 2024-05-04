import os
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from application_cal import Graph


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mockup Bank app for Pre VER.")
        self.configure(bg="#E2E2E2")
        self.df = pd.read_csv("test.csv")
        self.database_frame = None
        self.graph_frame = None
        self.canvas_sub1 = None
        self.canvas_sub2 = None
        self.init_components()


    def database_creating(self):
        if self.database_frame is None:
            if self.graph_frame is not None:
                self.graph_frame.destroy()
                self.graph_frame = None
            self.database_frame = tk.Frame(self, bg="white")
            tree = ttk.Treeview(self.database_frame)
            tree["columns"] = tuple(self.df.columns)
            tree["show"] = "headings"
            for column in self.df.columns:
                tree.column(column, width=30)
                tree.heading(column, text=column)

            for index, row in self.df.iterrows():
                tree.insert("", "end", values=tuple(row))

            scroll_bar = tk.Scrollbar(self.database_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scroll_bar.set)

            tree.pack(side=tk.LEFT, expand=True, fill="both", padx=10, pady=15)
            scroll_bar.pack(side=tk.RIGHT, fill="y")
            self.database_frame.pack(fill="both", expand=True)


    def on_select_hist(self, event=None):
        if self.canvas_sub1 is not None:
            self.canvas_sub1.get_tk_widget().destroy()
        selected = self.combobox_histrogram.get()
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        plot.plot(self.df[selected])
        self.canvas_sub1 = FigureCanvasTkAgg(fig, master=self.graph_sub_frame)
        self.canvas_sub1.draw()
        self.canvas_sub1.get_tk_widget().pack(side=tk.BOTTOM, expand=True, padx=10,pady=10)

    def on_select_pie(self, event=None):
        if self.canvas_sub2 is not None:
            self.canvas_sub2.get_tk_widget().destroy()
        selected = self.combobox_piechart.get()
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        plot.plot(self.df[selected])
        self.canvas_sub2 = FigureCanvasTkAgg(fig, master=self.graph_sub_frame2)
        self.canvas_sub2.draw()
        self.canvas_sub2.get_tk_widget().pack(side=tk.BOTTOM, expand=True, padx=10, pady=10)
    def graphframe_creating(self):
        if self.graph_frame is None:
            if self.database_frame is not None:
                self.database_frame.destroy()
                self.database_frame = None
            self.graph_frame = tk.Frame(self, bg='white')
            self.graph_frame.pack(expand=True,fill="both",padx=10,pady=10)

            self.graph_sub_frame = tk.Frame(self.graph_frame, bg='white')
            tk.Label(self.graph_sub_frame, text="Please choose attribute you want to show: ", fg="black", bg="white").pack(side=tk.TOP,expand=True, padx=5, pady=5)
            self.combobox_histrogram = ttk.Combobox(self.graph_sub_frame,
                                                    values=['age', 'balance', 'poutcome', 'education'],
                                                    state="readonly")
            self.combobox_histrogram.pack(side=tk.TOP,expand=True, padx=10, pady=10)
            self.combobox_histrogram.bind("<<ComboboxSelected>>", self.on_select_hist)

            self.graph_sub_frame2 = tk.Frame(self.graph_frame, bg='white')
            tk.Label(self.graph_sub_frame2, text="Please choose debt type you want to show: ", fg="black",
                     bg="white").pack(side=tk.TOP, expand=True, padx=5, pady=5)
            self.combobox_piechart = ttk.Combobox(self.graph_sub_frame2,
                                                    values=['default', 'housing', 'loan'],
                                                    state="readonly")
            self.combobox_piechart.pack(side=tk.TOP, expand=True, padx=10, pady=10)
            self.combobox_piechart.bind("<<ComboboxSelected>>", self.on_select_pie)


            self.graph_sub_frame.pack(side=tk.LEFT,expand=True)
            self.graph_sub_frame2.pack(side=tk.LEFT, expand=True)

    def exit(self):
        self.destroy()


    def top_option(self):
        top_frame = tk.Frame(self, bg="white")

        iso_button = tk.Button(master=top_frame, text="Personal", command="", fg="black", bg="red")
        iso_button.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)

        sum_graph_button = tk.Button(master=top_frame, text="Graph", command=self.graphframe_creating, fg="black", bg="white")
        sum_graph_button.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)

        dataset_button = tk.Button(master=top_frame, text="Database", command=self.database_creating, fg="black", bg="white")
        dataset_button.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)

        quit_button = tk.Button(master=top_frame, text="Exit",command=self.exit, fg="black", bg="white")
        quit_button.pack(side=tk.LEFT, expand=True, fill="both", padx=5, pady=5)

        return top_frame


    def init_components(self):
        option = self.top_option()
        option.pack(side=tk.TOP, expand=True, fill="both")


    def run(self):
        self.mainloop()

