from matplotlib.figure import Figure
import pandas as pd



class Graph():
    def __init__(self):
        self.df = pd.read_csv("test.csv")
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)


    def create_graph(self, value):
        if value == "age":
            bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 100]
            labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
            self.df['age_group'] = pd.cut(self.df['age'], bins=bins, labels=labels, right=False)
            age_group_counts = self.df['age_group'].value_counts().sort_index()
            self.plot.bar(age_group_counts.index, age_group_counts.values)
            self.plot.set_xlabel('age')
            self.plot.set_ylabel('frequency')
            self.plot.set_title('Age in Histogram')
            return self.fig