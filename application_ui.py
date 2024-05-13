import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import pandas as pd
from application_cal import Graph,Database

pad = {'padx': 5, 'pady': 5}


class Application(tk.Tk):
    """Main application class for the Bank Application GUI."""

    def __init__(self):
        """Initialize the Bank Application."""
        super().__init__()
        self.title("Bank Application")
        self.configure(bg="white")
        self.rowconfigure(0, weight=7)
        self.rowconfigure(1, weight=3)
        self.columnconfigure(0, weight=1)
        self.df = pd.read_csv("test.csv")
        self.personal_frame = None
        self.database_frame = None
        self.graph_frame = None
        self.graph = Graph()
        self.db = Database('test.csv')
        self.init_components()

    def destroy_canvas(self, frame):
        """Destroy canvas widgets within a frame."""
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Canvas):
                widget.destroy()

    def on_clear(self):
        """Destroy canvas widgets within a frame."""
        self.destroy_canvas(self.graph_sub_frame)
        self.destroy_canvas(self.graph_sub_frame2)
        self.destroy_canvas(self.static_info_sub_frame_sub)

    def check_personal_id(self, event):
        """Check if the entered personal ID is valid."""
        user_id = self.personal_id.get()
        if 0 < int(user_id) < len(self.df):
            self.search_button.configure(state='normal')
        else:
            self.search_button.configure(state='disabled')

    def on_click_search(self):
        """Display client information upon search."""
        user_id = self.personal_id.get()
        row_data = self.df.loc[int(user_id)-1]
        self.client_info.set(f'ID:{row_data["ID"]}, {row_data["age"]} years old'
        f', marital status: {row_data['marital']}, education level: {row_data['education']}'
        f'\njob: {row_data['job']} with balance ≈ {row_data['balance']}'
        f'\ndebt status: housing= {row_data['housing']}, loan= {row_data['loan']}, default= {row_data['default']}'
        f'\ncontact type: {row_data['contact']} previous outcome= {row_data['poutcome']}')
        temp_df = self.db.related_client(user_id)
        dataframe_string = temp_df.to_string(index=False)
        self.relative_client_info.delete('1.0',tk.END)
        self.relative_client_info.insert(tk.END, dataframe_string)

    def on_select_personal_hist(self, parent_value):
        """Display histogram based on selected attribute."""
        value = self.personal_combobox_histrogram.get()
        if value is not None:
            self.destroy_canvas(self.personal_sub_frame)
            self.graph.create_graph(value, self.personal_sub_frame)

    def on_select_graph_hist(self, parent_value):
        """Display histogram based on selected attribute in graph frame."""
        value = self.graph_combobox_histrogram.get()
        if value is not None:
            self.destroy_canvas(self.graph_sub_frame)
            self.graph.create_graph(value, self.graph_sub_frame)

    def on_select_stat(self, parent_value):
        """Display statistical graph based on selected attribute."""
        value = self.graph_stat_combobox.get()
        if value is not None:
            self.destroy_canvas(self.static_info_sub_frame_sub)
            self.graph.create_graph_stat(value, self.static_info_sub_frame_sub)

    def on_select_personal_pie(self, parent_value):
        """Display pie chart based on selected attribute."""
        value = self.personal_combobox_piechart.get()
        if value is not None:
            self.destroy_canvas(self.personal_sub_frame2)
            self.graph.create_graph(value, self.personal_sub_frame2)

    def on_select_graph_pie(self, parent_value):
        """Display pie chart based on selected attribute in graph frame."""
        value = self.graph_combobox_piechart.get()
        if value is not None:
            self.destroy_canvas(self.graph_sub_frame2)
            self.graph.create_graph(value, self.graph_sub_frame2)

    def personalframe_creating(self):
        """Create personal information frame."""
        if self.personal_frame is None:
            if self.database_frame is not None:
                self.database_frame.destroy()
                self.database_frame = None
            if self.graph_frame is not None:
                self.graph_frame.destroy()
                self.graph_frame = None
            self.personal_frame = tk.Frame(self, bg='white')
            self.personal_frame.rowconfigure(0, weight=1)
            self.personal_frame.rowconfigure(1, weight=1)
            self.personal_frame.rowconfigure(2, weight=6)
            self.personal_frame.rowconfigure(3, weight=2)
            self.personal_frame.columnconfigure(0, weight=1)
            self.personal_frame.columnconfigure(1, weight=1)

            personal_label_frame = tk.LabelFrame(self.personal_frame, text="Client's information", labelanchor='nw',
                                                 bg='white')
            personal_label_frame.rowconfigure(0, weight=1)
            personal_label_frame.columnconfigure(0, weight=1)
            personal_label_frame.columnconfigure(1, weight=2)
            personal_label_frame.columnconfigure(2, weight=2)
            personal_label_frame.columnconfigure(3, weight=1)
            label = tk.Label(personal_label_frame, text="Please enter client's id: ", bg='white')
            self.personal_id = tk.Entry(personal_label_frame)
            self.personal_id.bind('<KeyRelease>', self.check_personal_id)
            self.client_info = tk.StringVar()
            client_info_label = tk.Label(personal_label_frame, textvariable=self.client_info, bg='white')
            self.search_button = tk.Button(personal_label_frame, text='Search', bg='white', state='disabled', command=self.on_click_search)
            label.grid(row=0, column=0, **pad, sticky='ew')
            self.personal_id.grid(row=0, column=1, **pad, sticky='ew')
            client_info_label.grid(row=0, column=2, **pad, sticky='nws')
            self.search_button.grid(row=0, column=3, **pad, sticky='ew')
            personal_label_frame.grid(row=0, column=0, columnspan=2, **pad, sticky='ew')
            self.personal_frame.grid(row=1, column=0, **pad, sticky='news')

            self.personal_labelframe = tk.LabelFrame(self.personal_frame, bg='white')
            self.personal_labelframe.rowconfigure(0, weight=1)
            self.personal_labelframe.columnconfigure(0, weight=1)
            self.personal_labelframe.columnconfigure(1, weight=3)
            label = tk.Label(self.personal_labelframe, text="Please choose attribute you want to show: ", fg="black",
                             bg="white")
            label.grid(row=0, column=0, **pad, sticky='new')
            self.personal_combobox_histrogram = ttk.Combobox(self.personal_labelframe,
                                                             values=['age', 'balance', 'poutcome', 'education'],
                                                             state="readonly")
            self.personal_combobox_histrogram.grid(row=0, column=1, **pad, sticky='new')
            self.personal_combobox_histrogram.bind("<<ComboboxSelected>>", lambda event:self.on_select_personal_hist(self.personal_sub_frame))

            self.personal_labelframe2 = tk.LabelFrame(self.personal_frame, bg='white')
            self.personal_labelframe2.rowconfigure(0, weight=1)
            self.personal_labelframe2.columnconfigure(0, weight=1)
            self.personal_labelframe2.columnconfigure(1, weight=3)
            label2 = tk.Label(self.personal_labelframe2, text="Please choose debt type you want to show: ", fg="black",
                              bg="white")
            label2.grid(row=0, column=0, **pad, sticky='new')
            self.personal_combobox_piechart = ttk.Combobox(self.personal_labelframe2,
                                                           values=['default', 'housing', 'loan'],
                                                           state="readonly")
            self.personal_combobox_piechart.grid(row=0, column=1, **pad, sticky='new')
            self.personal_combobox_piechart.bind("<<ComboboxSelected>>", lambda event:self.on_select_personal_pie(self.personal_sub_frame2))

            self.personal_sub_frame = tk.Frame(self.personal_frame, bg='white')
            self.personal_sub_frame.rowconfigure(0, weight=1)
            self.personal_sub_frame.columnconfigure(0, weight=1)
            self.personal_sub_frame2 = tk.Frame(self.personal_frame, bg='white')
            self.personal_sub_frame2.rowconfigure(0, weight=1)
            self.personal_sub_frame2.columnconfigure(0, weight=1)

            most_related_frame = tk.LabelFrame(self.personal_frame, bg='white', text='Most related client', labelanchor='nw')
            most_related_frame.rowconfigure(0,weight=1)
            most_related_frame.columnconfigure(0, weight=1)
            self.relative_client_info = scrolledtext.ScrolledText(most_related_frame, wrap=tk.NONE)
            scroll_bar = tk.Scrollbar(most_related_frame, orient="horizontal", command=self.relative_client_info.xview)
            self.relative_client_info.configure(xscrollcommand=scroll_bar.set)
            self.relative_client_info.grid(row=1,column=0, **pad, sticky='news')
            scroll_bar.grid(row=0,column=0, **pad, sticky='news')
            self.personal_labelframe.grid(row=1, column=0, **pad, sticky='news')
            self.personal_labelframe2.grid(row=1, column=1, **pad, sticky='news')
            self.personal_sub_frame.grid(row=2, column=0, **pad, sticky='news')
            self.personal_sub_frame2.grid(row=2, column=1, **pad, sticky='news')
            most_related_frame.grid(row=3, column=0, columnspan=2, **pad, stick='news')

    def graphframe_creating(self):
        """Create graph frame."""
        if self.graph_frame is None:
            if self.database_frame is not None:
                self.database_frame.destroy()
                self.database_frame = None
            if self.personal_frame is not None:
                self.personal_frame.destroy()
                self.personal_frame = None
            self.graph_frame = tk.Frame(self, bg='white')
            self.graph_frame.rowconfigure(0, weight=1)
            self.graph_frame.rowconfigure(1, weight=1)
            self.graph_frame.rowconfigure(2, weight=1)
            self.graph_frame.rowconfigure(3, weight=1)
            self.graph_frame.columnconfigure(0, weight=1)
            self.graph_frame.columnconfigure(1, weight=1)

            self.graph_labelframe = tk.LabelFrame(self.graph_frame, bg='white')
            self.graph_labelframe.rowconfigure(0, weight=1)
            self.graph_labelframe.columnconfigure(0, weight=1)
            self.graph_labelframe.columnconfigure(1, weight=3)
            label = tk.Label(self.graph_labelframe, text="Please choose attribute you want to show: ", fg="black",
                             bg="white")
            label.grid(row=0, column=0, **pad, sticky='news')
            self.graph_combobox_histrogram = ttk.Combobox(self.graph_labelframe,
                                                             values=['age', 'balance', 'poutcome', 'education'],
                                                             state="readonly")
            self.graph_combobox_histrogram.grid(row=0, column=1, **pad, sticky='news')
            self.graph_combobox_histrogram.bind("<<ComboboxSelected>>", lambda event:self.on_select_graph_hist(self.graph_sub_frame))

            self.graph_labelframe2 = tk.LabelFrame(self.graph_frame, bg='white')
            self.graph_labelframe2.rowconfigure(0, weight=1)
            self.graph_labelframe2.columnconfigure(0, weight=1)
            self.graph_labelframe2.columnconfigure(1, weight=3)
            label2 = tk.Label(self.graph_labelframe2, text="Please choose debt type you want to show: ", fg="black",
                              bg="white")
            label2.grid(row=0, column=0, **pad, sticky='news')
            self.graph_combobox_piechart = ttk.Combobox(self.graph_labelframe2,
                                                           values=['default', 'housing', 'loan'],
                                                           state="readonly")
            self.graph_combobox_piechart.grid(row=0, column=1, **pad, sticky='news')
            self.graph_combobox_piechart.bind("<<ComboboxSelected>>", lambda event:self.on_select_graph_pie(self.graph_sub_frame2))

            self.graph_sub_frame = tk.Frame(self.graph_frame, bg='white')
            self.graph_sub_frame.rowconfigure(0, weight=1)
            self.graph_sub_frame.columnconfigure(0, weight=1)
            self.graph_sub_frame2 = tk.Frame(self.graph_frame, bg='white')
            self.graph_sub_frame2.rowconfigure(0, weight=1)
            self.graph_sub_frame2.columnconfigure(0, weight=1)

            self.static_info = tk.Frame(self.graph_frame, bg='white')
            self.static_info.rowconfigure(0, weight=1)
            self.static_info.columnconfigure(0, weight=1)
            self.static_info.columnconfigure(1, weight=1)
            self.static_info_sub_frame = tk.Frame(self.static_info, bg='white')
            self.static_info_sub_frame.rowconfigure(0, weight=1)
            self.static_info_sub_frame.rowconfigure(1, weight=4)
            self.static_info_sub_frame.columnconfigure(0, weight=1)
            self.static_label_frame = tk.LabelFrame(self.static_info_sub_frame,bg='white', text='Graph Type', labelanchor='nw')
            self.static_label_frame.rowconfigure(0,weight=1)
            self.static_label_frame.columnconfigure(0,weight=1)
            self.static_label_frame.columnconfigure(1, weight=4)
            self.static_label_frame.grid(row=0,column=0,**pad,sticky='news')
            label = tk.Label(self.static_label_frame, text='Choose your graph type: ',bg='white')
            self.graph_stat_combobox = ttk.Combobox(self.static_label_frame, values=['BarPlot','Heatmap','ScatterPlot'])
            label.grid(row=0,column=0,**pad,sticky='nws')
            self.graph_stat_combobox.grid(row=0,column=1,**pad,sticky='news')
            self.graph_stat_combobox.bind('<<ComboboxSelected>>', lambda event:self.on_select_stat(self.static_info_sub_frame_sub))
            self.static_info_sub_frame_sub = tk.Frame(self.static_info_sub_frame,bg='white')
            self.static_info_sub_frame_sub.rowconfigure(0, weight=1)
            self.static_info_sub_frame_sub.columnconfigure(0,weight=1)
            self.static_info_sub_frame_sub.grid(row=1,column=0,**pad,sticky='news')
            self.static_info_sub_frame.grid(row=0,column=0,**pad,sticky='news')
            self.static_info_sub_frame2 = tk.Text(self.static_info, wrap=tk.NONE)
            age_stats = self.df['age'].describe()
            balance_stats = self.df['balance'].describe()
            correlation = self.df['age'].corr(self.df['balance'])
            self.static_info_sub_frame2.insert(tk.END, "Descriptive Statistics of Age:\n")
            self.static_info_sub_frame2.insert(tk.END, "Age describes the ages of individuals in the dataset.\n\n")
            self.static_info_sub_frame2.insert(tk.END, str(age_stats) + "\n\n")
            self.static_info_sub_frame2.insert(tk.END, "Descriptive Statistics of Balance:\n")
            self.static_info_sub_frame2.insert(tk.END, "Balance describes the financial balance of individuals in the dataset.\n\n")
            self.static_info_sub_frame2.insert(tk.END, str(balance_stats) + "\n\n")
            self.static_info_sub_frame2.insert(tk.END, f'Corrlation: {correlation}')
            self.static_info_sub_frame2.grid(row=0,column=1,**pad,sticky='news')
            self.graph_labelframe.grid(row=0,column=0,**pad,sticky='news')
            self.graph_labelframe2.grid(row=0, column=1, **pad, sticky='news')
            self.graph_sub_frame.grid(row=1, column=0, **pad, sticky='news')
            self.graph_sub_frame2.grid(row=1, column=1, **pad, sticky='news')
            self.static_info.grid(row=2,column=0,columnspan=2,**pad,sticky='news')
            self.graph_frame.grid(row=1,column=0,**pad,sticky='news')

            clear_button = tk.Button(self.graph_frame, text='Clear', command=self.on_clear)
            clear_button.grid(row=3,column=1,**pad,sticky='ew')

    def check_client_id(self, event):
        """Check client's ID"""
        user_id = self.client_id.get()
        if 0 < int(user_id) < len(self.df):
            self.remove_button.configure(state='normal')
        else:
            self.remove_button.configure(state='disabled')

    def sort_client(self):
        """Check button"""
        sorted_attribute = self.sort_attribute.get()
        if sorted_attribute is None:
            self.sort_button.configure(state='disabled')
        else:
            temp_df = self.db.sort_value(sorted_attribute)
            temp_string = temp_df.to_string(index=False)
            self.data_show.delete('1.0', tk.END)
            self.data_show.insert(tk.END, temp_string)
            messagebox.showinfo(message="Success!")

    def remove_client(self):
        """Check button"""
        user_id = self.client_id.get()
        if user_id is None:
            self.remove_button.configure(state='disabled')
        else:
            self.db.remove_client(user_id)
            self.data_show.delete('1.0', tk.END)
            self.data_show.insert(tk.END, self.df.to_string(index=False))
            messagebox.showinfo(message="Success!")

    def sort_client_button(self):
        """Initialize toplevel for sort client from database"""
        sort_window = tk.Toplevel(self)
        sort_window.title('Remove Client')
        sort_window.configure(bg='white')
        sort_window.rowconfigure(0, weight=1)
        sort_window.columnconfigure(0, weight=1)
        sort_frame = tk.Frame(sort_window)
        sort_frame.configure(bg='white')
        sort_frame.rowconfigure(0, weight=4)
        sort_frame.rowconfigure(1, weight=1)
        sort_frame.columnconfigure(0, weight=1)
        sort_frame.columnconfigure(1, weight=2)
        sort_frame.columnconfigure(2, weight=1)

        self.client_id = tk.StringVar()
        label = tk.Label(sort_frame, text="Press choose attribute you want to sort: ", bg='white')
        self.sort_attribute = ttk.Combobox(sort_frame, values=self.df.columns.tolist())
        self.sort_button = tk.Button(sort_frame, text='Sort', bg='white', state='disabled',
                                       command=self.sort_client)
        self.sort_attribute.bind('<<ComboboxSelected>>', self.sort_button.configure(state='normal'))
        quit_button = tk.Button(sort_frame, text='Quit', command=sort_window.destroy, bg='white')

        label.grid(row=0, column=0, **pad, sticky='nws')
        self.sort_attribute.grid(row=0, column=1, **pad, sticky='news')
        self.sort_button.grid(row=0, column=2, **pad, sticky='news')
        quit_button.grid(row=1, column=2, **pad, sticky='news')

        sort_frame.grid(row=0, column=0, **pad, sticky='news')

    def remove_client_button(self):
        """Initialize toplevel for remove client from database"""
        remove_window = tk.Toplevel(self)
        remove_window.title('Remove Client')
        remove_window.configure(bg='white')
        remove_window.rowconfigure(0, weight=1)
        remove_window.columnconfigure(0, weight=1)
        remove_frame = tk.Frame(remove_window)
        remove_frame.configure(bg='white')
        remove_frame.rowconfigure(0, weight=4)
        remove_frame.rowconfigure(1, weight=1)
        remove_frame.columnconfigure(0, weight=1)
        remove_frame.columnconfigure(1, weight=2)
        remove_frame.columnconfigure(2, weight=1)

        self.client_id = tk.StringVar()
        label = tk.Label(remove_frame, text="Press client's ID you want to remove: ", bg='white')
        user_entry = tk.Entry(remove_frame, textvariable=self.client_id)
        user_entry.bind("<KeyRelease>", self.check_client_id)
        self.remove_button = tk.Button(remove_frame, text='Remove', bg='white', state='disabled',
                                       command=self.remove_client)
        quit_button = tk.Button(remove_frame, text='Quit', command=remove_window.destroy, bg='white')

        label.grid(row=0, column=0, **pad, sticky='nws')
        user_entry.grid(row=0, column=1, **pad, sticky='news')
        self.remove_button.grid(row=0, column=2, **pad, sticky='news')
        quit_button.grid(row=1, column=2, **pad, sticky='news')

        remove_frame.grid(row=0, column=0, **pad, sticky='news')

    def clear_info(self):
        """Clear all info that inform already"""
        for widget in [self.age_enter, self.balance_enter, self.previous_enter,
                       self.job_combobox, self.marital_combobox, self.education_combobox,
                       self.contact_combobox, self.poutcome_combobox, self.default_combobox,
                       self.housing_combobox, self.loan_combobox]:
            widget.delete(0, tk.END)
        self.add_button.configure(state='disabled')

    def add_client(self):
        """Get variable values to create new client data"""
        age = self.age_enter.get()
        balance = self.balance_enter.get()
        previous = self.previous_enter.get()
        job = self.job_combobox.get()
        marital = self.marital_combobox.get()
        edu = self.education_combobox.get()
        contact = self.contact_combobox.get()
        poutcome = self.poutcome_combobox.get()
        default = self.default_combobox.get()
        housing = self.housing_combobox.get()
        loan = self.loan_combobox.get()
        self.db.add_client(age, balance, previous, job, marital, edu, contact, poutcome, default, housing, loan)
        self.data_show.delete('1.0', tk.END)
        self.data_show.insert(tk.END, self.df.to_string(index=False))
        messagebox.showinfo(message="Success!")

    def check_entry(self, event):
        """Check entry in Toplevel"""
        entry = event.widget
        value = entry.get()

        if not value.isdigit() or int(value) <= 0 or int(value) > 100:
            entry.config(foreground='red')
            self.add_button.configure(state='disabled')
        else:
            entry.config(foreground='black')

        if (self.age_enter.cget('fg') == 'black'
                and self.balance_enter.cget('fg') == 'black'
                and self.previous_enter.cget('fg') == 'black'
                and self.job_combobox.get() and self.marital_combobox.get()
                and self.education_combobox.get() and self.contact_combobox.get()
                and self.poutcome_combobox.get() and self.default_combobox.get()
                and self.housing_combobox.get() and self.loan_combobox.get()):
            self.add_button.configure(state='normal')
        else:
            self.add_button.configure(state='disabled')

    def check_entry2(self, event):
        """Check entry in Toplevel"""
        entry = event.widget
        value = entry.get()

        if not value.isdigit() or int(value) <= -5000 or int(value) > 10000:
            entry.config(foreground='red')
            self.add_button.configure(state='disabled')
        else:
            entry.config(foreground='black')

        if (self.age_enter.cget('fg') == 'black'
                and self.balance_enter.cget('fg') == 'black'
                and self.previous_enter.cget('fg') == 'black'
                and self.job_combobox.get() and self.marital_combobox.get()
                and self.education_combobox.get() and self.contact_combobox.get()
                and self.poutcome_combobox.get() and self.default_combobox.get()
                and self.housing_combobox.get() and self.loan_combobox.get()):
            self.add_button.configure(state='normal')
        else:
            self.add_button.configure(state='disabled')

    def check_entry3(self, event):
        """Check entry in Toplevel"""
        entry = event.widget
        value = entry.get()

        if not value.isdigit() or int(value) < 0 or int(value) > 50:
            entry.config(foreground='red')
            self.add_button.configure(state='disabled')
        else:
            entry.config(foreground='black')

        if (self.age_enter.cget('fg') == 'black'
                and self.balance_enter.cget('fg') == 'black'
                and self.previous_enter.cget('fg') == 'black'
                and self.job_combobox.get() and self.marital_combobox.get()
                and self.education_combobox.get() and self.contact_combobox.get()
                and self.poutcome_combobox.get() and self.default_combobox.get()
                and self.housing_combobox.get() and self.loan_combobox.get()):
            self.add_button.configure(state='normal')
        else:
            self.add_button.configure(state='disabled')

    def check_input(self, event):
        """Check input"""
        if (self.age_enter.cget('fg') == 'black'
                and self.balance_enter.cget('fg') == 'black'
                and self.previous_enter.cget('fg') == 'black'
                and self.job_combobox.get() and self.marital_combobox.get()
                and self.education_combobox.get() and self.contact_combobox.get()
                and self.poutcome_combobox.get() and self.default_combobox.get()
                and self.housing_combobox.get() and self.loan_combobox.get()):
            self.add_button.configure(state='normal')
        else:
            self.add_button.configure(state='disabled')

    def add_client_button(self):
        """Toplevel for database part to add client to database"""
        add_window = tk.Toplevel(self)
        add_window.title("Add Client")
        add_window.configure(bg='white')
        add_window.rowconfigure(0, weight=1)
        add_window.columnconfigure(0, weight=1)
        add_frame = tk.Frame(add_window)
        add_frame.configure(bg='white')
        for i in range(13):
            add_frame.rowconfigure(i, weight=1)
        add_frame.columnconfigure(0, weight=1)
        add_frame.columnconfigure(1, weight=3)
        info_label = tk.Label(master=add_frame, text="Please enter only lower-case alphabet or number or NA if you"
                                                     " don't know this info", bg='white')
        age_label = tk.Label(master=add_frame, text="Enter client's age(pick between 0-100): ", bg='white')
        age_var = tk.IntVar()
        self.age_enter = tk.Entry(master=add_frame, textvariable=age_var)
        balance_label = tk.Label(master=add_frame,
                                 text="Enter client's average year balance(pick between -5000-100000): ", bg='white')
        balance_var = tk.IntVar()
        self.balance_enter = tk.Entry(master=add_frame, textvariable=balance_var)
        previous_label = tk.Label(master=add_frame,
                                  text="Enter number of old contacts of this client(pick between 0-50): ", bg='white')
        previous_var = tk.IntVar()
        self.previous_enter = tk.Entry(master=add_frame, textvariable=previous_var)
        job_label = tk.Label(master=add_frame, text="Choose client's job: ", bg='white')
        job_var = tk.StringVar()
        self.job_combobox = ttk.Combobox(master=add_frame, values=["admin.", "unknown"
            , "unemployed", "management", "housemaid", "entrepreneur", "student"
            , "blue-collar", "self-employed", "retired", "technician", "services"]
                                         , textvariable=job_var)
        marital_label = tk.Label(master=add_frame, text="Choose client's marital information: ", bg='white')
        marital_var = tk.StringVar()
        self.marital_combobox = ttk.Combobox(master=add_frame, values=["married"
            , "divorced", "single"], textvariable=marital_var)
        education_label = tk.Label(master=add_frame, text="Choose client's education level: ", bg='white')
        education_var = tk.StringVar()
        self.education_combobox = ttk.Combobox(master=add_frame, values=["unknown"
            , "secondary", "primary", "tertiary"], textvariable=education_var)
        contact_label = tk.Label(master=add_frame, text="Choose client contact communication type: ", bg='white')
        contact_var = tk.StringVar()
        self.contact_combobox = ttk.Combobox(master=add_frame, values=["unknown"
            , "telephone", "cellular"], textvariable=contact_var)
        poutcome_label = tk.Label(master=add_frame, text="Choose outcome of the previous marketing campaign of this "
                                                         "client: ", bg='white')
        poutcome_var = tk.StringVar()
        self.poutcome_combobox = ttk.Combobox(master=add_frame, values=["unknown"
            , "other", "failure", "success"], textvariable=poutcome_var)
        default_label = tk.Label(master=add_frame, text="Does client have debt?: ", bg='white')
        default_var = tk.StringVar()
        self.default_combobox = ttk.Combobox(master=add_frame, values=["yes", "no"], textvariable=default_var)
        housing_label = tk.Label(master=add_frame, text="Does client have housing loan?: ", bg='white')
        housing_var = tk.StringVar()
        self.housing_combobox = ttk.Combobox(master=add_frame, values=["yes", "no"], textvariable=housing_var)
        loan_label = tk.Label(master=add_frame, text="Does client have personal loan?: ", bg='white')
        loan_var = tk.StringVar()
        self.loan_combobox = ttk.Combobox(master=add_frame, values=["yes", "no"], textvariable=loan_var)
        clear_button = tk.Button(master=add_frame, text='Clear', bg='white', fg='black', command=self.clear_info)
        self.add_button = tk.Button(master=add_frame, text='Add', bg='white', fg='black', state='disabled',
                                    command=self.add_client)
        quit_button = tk.Button(master=add_frame, text='Quit', bg='white', fg='black', command=add_window.destroy)
        widget_list = [self.age_enter, self.balance_enter, self.previous_enter
            , self.job_combobox, self.marital_combobox, self.education_combobox
            , self.contact_combobox, self.poutcome_combobox
            , self.default_combobox, self.housing_combobox, self.loan_combobox]
        func_list = [self.check_entry, self.check_entry2, self.check_entry3]
        widget_n = 0
        for widget in widget_list:
            if widget_n < 3:
                widget.bind("<FocusOut>", func_list[widget_n])
                widget_n += 1
            else:
                widget.bind('<<ComboboxSelected>>', self.check_input)
        info_list = [info_label, clear_button, age_label, self.age_enter
            , balance_label, self.balance_enter, previous_label
            , self.previous_enter, job_label, self.job_combobox, marital_label
            , self.marital_combobox, education_label, self.education_combobox
            , contact_label, self.contact_combobox, poutcome_label
            , self.poutcome_combobox, default_label, self.default_combobox
            , housing_label, self.housing_combobox, loan_label, self.loan_combobox
            , self.add_button, quit_button]
        l_row = 0
        for index, widget in enumerate(info_list):
            if index % 2 == 0:
                widget.grid(row=l_row, column=0, **pad, sticky='nws')
            else:
                widget.grid(row=l_row, column=1, **pad, sticky='news')
                l_row += 1
        add_frame.grid(row=0, column=0, **pad, sticky='news')

    def database_creating(self):
        """Initialize database part"""
        if self.database_frame is None:
            if self.graph_frame is not None:
                self.graph_frame.destroy()
                self.graph_frame = None
            if self.personal_frame is not None:
                self.personal_frame.destroy()
                self.personal_frame = None
            self.database_frame = tk.Frame(self, bg="white")
            self.database_frame.rowconfigure(0, weight=1)
            self.database_frame.rowconfigure(1, weight=4)
            self.database_frame.columnconfigure(0, weight=1)

            label_frame = tk.LabelFrame(master=self.database_frame, text='Client Information', labelanchor='nw',
                                        bg='white')
            label_frame.rowconfigure(0, weight=1)
            label_frame.columnconfigure(0, weight=7)
            label_frame.columnconfigure(1, weight=1)
            label_frame.columnconfigure(2, weight=1)
            label_frame.columnconfigure(3, weight=1)
            label_frame.columnconfigure(4, weight=1)
            button = tk.Button(master=label_frame, text='add client', fg='black', bg='white',
                               command=self.add_client_button)
            button2 = tk.Button(master=label_frame, text='remove client', fg='black', bg='white',
                                command=self.remove_client_button)
            # button3 = tk.Button(master=label_frame, text='filter', fg='black', bg='white', command='')
            button4 = tk.Button(master=label_frame, text='sort', fg='black', bg='white', command=self.sort_client_button)
            button.grid(row=0, column=1, **pad, sticky='news')
            button2.grid(row=0, column=2, **pad, sticky='news')
            # button3.grid(row=0, column=3, **pad, sticky='news')
            button4.grid(row=0, column=4, **pad, sticky='news')

            self.data_show = scrolledtext.ScrolledText(master=self.database_frame, wrap=tk.NONE)
            dataframe_string = self.df.to_string(index=False)
            self.data_show.insert(tk.END, dataframe_string)

            scroll_bar = tk.Scrollbar(self.database_frame, orient="horizontal", command=self.data_show.xview)
            self.data_show.configure(xscrollcommand=scroll_bar.set)

            label_frame.grid(row=0, column=0, **pad, sticky='news')
            self.data_show.grid(row=1, column=0, **pad, sticky='news')
            scroll_bar.grid(row=1, column=0, sticky='ews', **pad)
            self.database_frame.grid(row=1, column=0, **pad, sticky='news')

    def exit(self):
        """Use to create exit the program"""
        choice = messagebox.askyesno(title='Warning', message='Do you really want to quit?')
        if choice:
            self.destroy()

    def top_option(self):
        """Initialize top option for user"""
        top_frame = tk.Frame(self, bg="white")
        top_frame.rowconfigure(0, weight=1)
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)
        top_frame.columnconfigure(3, weight=1)

        personal_button = tk.Button(top_frame, text='Personal', command=self.personalframe_creating, bg='white')
        personal_button.grid(row=0, column=0, sticky='news', **pad)

        sum_graph_button = tk.Button(top_frame, text="Graph", command=self.graphframe_creating, bg="white")
        sum_graph_button.grid(row=0, column=1, sticky='news', **pad)

        dataset_button = tk.Button(top_frame, text="Database", command=self.database_creating, bg="white")
        dataset_button.grid(row=0, column=2, sticky='news', **pad)

        quit_button = tk.Button(top_frame, text="Exit", command=self.exit, bg="white")
        quit_button.grid(row=0, column=3, sticky='news', **pad)

        return top_frame

    def init_components(self):
        """Initialize components of the application."""
        option = self.top_option()
        option.grid(row=0, column=0, sticky='news', **pad)
        text = tk.Text(self, wrap=tk.NONE)
        text.grid(row=1, column=0, **pad, sticky='news')

    def run(self):
        """Use this function to run this class"""
        self.mainloop()
