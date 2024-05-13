import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

pad = {'padx':5,'pady':5}

class Graph():
    def __init__(self):
        self.df = pd.read_csv("test.csv")

    def create_graph(self, value, parent_value):
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        if value == "age":
            bins = [num for num in range(0, 110, 10)]
            labels = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100']
            self.df['age_group'] = pd.cut(self.df['age'], bins=bins, labels=labels, right=False)
            age_group_counts = self.df['age_group'].value_counts().sort_index()
            plot.bar(age_group_counts.index, age_group_counts.values, color='grey')
            plot.set_xlabel('age')
            plot.set_ylabel('frequency')
            plot.set_title('Frequency of Age')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')
        elif value == 'balance':
            bins = [num for num in range(-3000, 39000, 3000)]
            labels = ['0', '3k', '6k', '9k', '12k', '15k',
                      '18k', '21k', '24k', '27k', '30k',
                      '33k', '36k']
            self.df['balance_group'] = pd.cut(self.df['balance'], bins=bins, labels=labels, right=False)
            balance_group_counts = self.df['balance_group'].value_counts().sort_index()
            plot.bar(balance_group_counts.index, balance_group_counts.values, color='grey')
            plot.set_xlabel('balance')
            plot.set_ylabel('frequency')
            plot.set_title('Frequency of Balance')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')
        elif value == 'poutcome':
            poutcome_group_counts = self.df['poutcome'].value_counts().sort_index()
            plot.bar(poutcome_group_counts.index, poutcome_group_counts.values, color='grey')
            plt.xlabel('Previous campaign outcome')
            plt.ylabel('Frequency')
            plt.title('Frequency of Previous outcome')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')
        elif value == 'education':
            education_group_counts = self.df['education'].value_counts().sort_index()
            plot.bar(education_group_counts.index, education_group_counts.values, color='grey')
            plt.xlabel('Education Level')
            plt.ylabel('Frequency')
            plt.title('Frequency of Education Levels')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')
        elif value == 'default':
            default_counts = self.df['default'].value_counts()
            fig, ax = plt.subplots()
            max_value_index = default_counts.idxmax()
            colors = ['orange' if index == max_value_index else 'grey' for index in default_counts.index]

            ax.pie(default_counts, labels=default_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')
        elif value == 'housing':
            housing_counts = self.df['housing'].value_counts()
            fig, ax = plt.subplots()
            max_value_index = housing_counts.idxmax()
            colors = ['orange' if index == max_value_index else 'grey' for index in housing_counts.index]

            ax.pie(housing_counts, labels=housing_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')
        elif value == 'loan':
            loan_counts = self.df['loan'].value_counts()
            fig, ax = plt.subplots()
            max_value_index = loan_counts.idxmax()
            colors = ['orange' if index == max_value_index else 'grey' for index in loan_counts.index]

            ax.pie(loan_counts, labels=loan_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, padx=5, pady=5, sticky='news')

    def create_graph_stat(self ,value, parent_value):
        selected_column = self.df[['age', 'balance']].copy()
        if value == 'BarPlot':
            fig, ax = plt.subplots()
            ax.bar(selected_column['age'], selected_column['balance'])
            ax.set_xlabel('Age')
            ax.set_ylabel('Balance')
            ax.set_title('Bar Plot of Age vs. Balance')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0,column=0, **pad, sticky='news')
        elif value == 'Heatmap':
            fig, ax = plt.subplots()
            sns.heatmap(selected_column.corr(), annot=True, cmap='coolwarm', ax=ax)
            ax.set_title('Heatmap of Age vs. Balance')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0,column=0, **pad, sticky='news')
        elif value == 'ScatterPlot':
            fig, ax = plt.subplots()
            ax.scatter(selected_column['age'], selected_column['balance'])
            ax.set_xlabel('Age')
            ax.set_ylabel('Balance')
            ax.set_title('Scatter Plot of Age vs. Balance')
            canvas = FigureCanvasTkAgg(fig, master=parent_value)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0,column=0, **pad, sticky='news')


class Database():
    def __init__(self, file):
        self.df = pd.read_csv(file)

    def add_client(self, age, balance, ncon, job, marital, edu, cont, pout, d, h, l):
        num = len(self.df) + 1
        new_row = {'ID': num, 'age': age, 'balance': balance, 'previous': ncon, 'job': job, 'marital': marital,
                   'education': edu, 'contact': cont, 'poutcome': pout, 'default': d, 'housing': h, 'loan': l}
        new_df = pd.DataFrame(new_row, index=[0])
        df = pd.concat([self.df, new_df], ignore_index=True)
        df.to_csv('test.csv', index=False)

    def remove_client(self, index):
        df = self.df.drop(int(index)-1)
        df = df.reset_index(drop=True)
        df['ID'] = df.index + 1
        df.to_csv('test.csv', index=False)

    def sort_value(self, value):
        df = self.df.sort_values(by=value)
        return df

    def related_client(self, client_id):
        temp_df = self.df.copy()
        row_data = temp_df.loc[int(client_id) - 1]
        target_row = pd.Series({'ID':row_data['ID'],'age': row_data['age'], 'job': row_data['job']
            , 'marital': row_data['marital'], 'education': row_data['education']
            , 'default': row_data['default'], 'balance': row_data['balance'], 'housing': row_data['housing']
            , 'loan': row_data['loan'], 'contact': row_data['contact']
            , 'previous': row_data['previous'], 'poutcome': row_data['poutcome']
            , 'y': row_data['y']})
        temp_df['unrelated'] = temp_df.apply(lambda row: sum(row != target_row), axis=1)
        sorted_df = temp_df[temp_df['unrelated'] <= 6].sort_values(by='unrelated')
        return sorted_df


