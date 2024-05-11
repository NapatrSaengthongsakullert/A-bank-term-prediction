
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Graph():
    def __init__(self):
        self.df = pd.read_csv("test.csv")
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.fig.add_subplot(111)

    def create_graph(self, value, parent):
        if value == "age":
            bins = [num for num in range(0, 110, 10)]
            labels = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']
            self.df['age_group'] = pd.cut(self.df['age'], bins=bins, labels=labels, right=False)
            age_group_counts = self.df['age_group'].value_counts().sort_index()
            self.plot.bar(age_group_counts.index, age_group_counts.values, color='grey')
            self.plot.set_xlabel('age')
            self.plot.set_ylabel('frequency')
            self.plot.set_title('Frequency of Age')
            return  self.fig
        elif value == 'balance':
            bins = [num for num in range(-3000, 39000, 3000)]
            labels = ['0', '3000', '6000', '9000', '12000', '15000',
                      '18000', '21000', '24000', '27000', '30000',
                      '33000', '36000']
            self.df['balance_group'] = pd.cut(self.df['balance'], bins=bins, labels=labels, right=False)
            balance_group_counts = self.df['balance_group'].value_counts().sort_index()
            self.plot.bar(balance_group_counts.index, balance_group_counts.values, color='grey')
            self.plot.set_xlabel('balance')
            self.plot.set_ylabel('frequency')
            self.plot.set_title('Frequency of Balance')
            return  self.fig
        elif value == 'poutcome':
            self.df['poutcome'].value_counts().plot(kind='bar', color='grey')
            plt.xlabel('Previous campaign outcome')
            plt.ylabel('Frequency')
            plt.title('Frequency of Previous outcome')
            return plt.gcf()
        elif value == 'education':
            education_counts = self.df['education'].value_counts()
            bar_plot = education_counts.plot(kind='bar', color='grey')
            plt.xlabel('Education Level')
            plt.ylabel('Frequency')
            plt.title('Frequency of Education Levels')
            return plt.gcf()
        elif value == 'default':
            default_counts = self.df['default'].value_counts()
            fig, ax = plt.subplots()
            max_value_index = default_counts.idxmax()
            colors = ['orange' if index == max_value_index else 'grey' for index in default_counts.index]

            ax.pie(default_counts, labels=default_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')

            return fig
        elif value == 'housing':
            housing_counts = self.df['housing'].value_counts()
            fig, ax = plt.subplots()
            max_value_index = housing_counts.idxmax()
            colors = ['orange' if index == max_value_index else 'grey' for index in housing_counts.index]

            ax.pie(housing_counts, labels=housing_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')

            return fig
        elif value == 'loan':
            loan_counts = self.df['loan'].value_counts()
            fig, ax = plt.subplots()
            max_value_index = loan_counts.idxmax()
            colors = ['orange' if index == max_value_index else 'grey' for index in loan_counts.index]

            ax.pie(loan_counts, labels=loan_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')

            return fig



class Database():
    def __init__(self, file):
        self.df = pd.read_csv(file)

    def add_client(self, age, balance, ncon, job, marital, edu, cont, pout, d, h, l):
        num = len(self.df) + 1
        # สร้าง DataFrame ที่จะเพิ่มเข้าไป
        new_row = {'ID': num, 'age': age, 'balance': balance, 'previous': ncon, 'job': job, 'marital': marital,
                   'education': edu, 'contact': cont, 'poutcome': pout, 'default': d, 'housing': h, 'loan': l}
        # สร้าง DataFrame จากแถวใหม่ที่จะเพิ่ม
        new_df = pd.DataFrame(new_row, index=[0])
        # เพิ่มแถวใหม่ใน DataFrame โดยใช้ pd.concat()
        df = pd.concat([self.df, new_df], ignore_index=True)
        # บันทึก DataFrame กลับเป็นไฟล์ CSV
        df.to_csv('test.csv', index=False)

    def remove_client(self, index):
        df = self.df.drop(int(index)-1)
        df = df.reset_index(drop=True)
        df['ID'] = df.index + 1
        df.to_csv('test.csv', index=False)

    def config_client(self):
        pass

    def filter(self):
        pass

