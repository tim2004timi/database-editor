from sqlite3 import connect
from os import listdir
from pandas import read_sql_query
from matplotlib.pyplot import subplots, savefig
from PIL import Image, ImageTk
from time import gmtime, strftime

import customtkinter as CTk
import tkinter
import sqlite3 as sq

from windows.create_database_window import CreateDatabaseWindow
from windows.parent_window import ParentWindow
from windows.image_label import ImageLabel


class StartWindow(ParentWindow):
    def __init__(self):
        super().__init__()

        # Список баз данных
        self.databases_list = listdir("databases")
        self.databases_option_menu = CTk.CTkOptionMenu(master=self, values=self.databases_list, width=200)
        self.databases_option_menu.place(relx=.5, rely=.4, anchor=tkinter.CENTER)

        # Кнопка подключения
        self.connect_button = CTk.CTkButton(master=self, text="Подключиться", width=200, command=self.main_window)
        self.connect_button.place(relx=.5, rely=.47, anchor=tkinter.CENTER)

        # Кнопка создания новой базы данных
        self.create_database_button = CTk.CTkButton(master=self, text="Создать базу данных", width=200,
                                                    command=self.create_database_window)
        self.create_database_button.place(relx=.5, rely=.54, anchor=tkinter.CENTER)

    def main_window(self):
        self.destroy()
        name_database = self.databases_option_menu.get()
        with connect(f"databases/{name_database}") as connection:
            MainWindow(name_database, connection).mainloop()

    def create_database_window(self):
        CreateDatabaseWindow(self.databases_option_menu)


class MainWindow(ParentWindow):
    def __init__(self, name_database, connection: sq.Connection):
        super().__init__()
        self.canvas = self.image = self.photo = None
        self.protocol("WM_DELETE_WINDOW", lambda: exit())

        self.name_database = name_database
        self.connection = connection

        self.cursor = connection.cursor()
        self.cursor.execute("""
        SELECT 
            name
        FROM 
            sqlite_schema
        WHERE 
            type ='table' AND 
            name NOT LIKE 'sqlite_%';""")
        self.tables_list = list(map(lambda x: x[0], self.cursor.fetchall()))

        # Название
        font1 = CTk.CTkFont(family="Arial", size=24, weight="bold")
        self.name = CTk.CTkLabel(master=self, text=self.name_database.split(".")[0], font=font1, text_color="#667")
        self.name.place(relx=.5, rely=.05, anchor=tkinter.CENTER)

        # Страницы выбора
        self.tabview = CTk.CTkTabview(master=self, width=560, height=480)
        self.tabview.place(relx=.35, rely=.07)

        self.tab_1 = self.tabview.add("Запрос")
        self.tab_2 = self.tabview.add("Данные")

        # Текст запроса
        font3 = CTk.CTkFont(family="Arial", size=18)
        self.textbox = CTk.CTkTextbox(master=self.tab_1, width=537, height=425, border_width=2, corner_radius=1,
                                      border_color="#8080a0", font=font3, text_color="#555")
        self.textbox.place(x=5, y=0)

        # Таблицы
        font2 = CTk.CTkFont(family="Arial", size=12, weight="bold")
        self.name = CTk.CTkLabel(master=self, text="Таблицы:", text_color="#555", font=font2)
        self.name.place(relx=.05, rely=.1)

        self.tables_option_menu = CTk.CTkOptionMenu(master=self, values=self.tables_list, width=200)
        self.tables_option_menu.place(relx=.05, rely=.145)

        # Вывести таблицу
        self.output_table_button = CTk.CTkButton(master=self, text="Вывести данные", width=200,
                                                 command=self.output_table)
        self.output_table_button.place(relx=.05, rely=.245)

        # Записать в файл
        self.write_file_button = CTk.CTkButton(master=self, text="Записать в csv", width=200, command=self.write_file)
        self.write_file_button.place(relx=.05, rely=.345)

        # Гифка
        self.image_label = ImageLabel(master=self)
        self.image_label.place(x=79, y=375)
        self.image_label.load('g.gif')

        # SQL запрос
        self.query_button = CTk.CTkButton(master=self, text="SQL запрос", width=200, command=self.query)
        self.query_button.place(relx=.555, rely=.91)

        # Назад
        self.back_button = CTk.CTkButton(master=self, text="Назад", width=50, fg_color="gray", command=self.back)
        self.back_button.place(x=5, y=5)

    def back(self):
        self.destroy()
        StartWindow().mainloop()

    def output_image(self, df):
        fig, ax = subplots()
        ax.axis('off')
        ax.axis('tight')
        ax.table(cellText=df.values, colLabels=df.columns, loc='center')
        savefig('table.png')

        self.canvas = tkinter.Canvas(master=self.tab_2, width=665, height=530)
        self.image = Image.open("table.png")
        self.image = self.image.resize((667, 532))
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
        self.canvas.place(x=5, y=0)

        self.tabview.set("Данные")

    def output_table(self, query=None):
        try:
            if not query:
                query = f"SELECT * FROM {self.tables_option_menu.get()}"
            df = read_sql_query(query, self.connection)
            print(df)

            if df.all:
                self.output_image(df)
        except Exception as e:
            print(e)

    def write_file(self):
        try:
            table = self.tables_option_menu.get()
            current_time = strftime("_%Y_%m_%d_%H-%M-%S", gmtime())

            query = f"SELECT * FROM {table}"
            df = read_sql_query(query, self.connection)
            df.to_csv(f"saves/{table + current_time}.csv", sep=',', index=False)
        except Exception as e:
            print(e)

    def query(self):
        try:
            self.output_table(self.textbox.get("0.0", "end"))
            self.connection.commit()
        except Exception as e:
            print(e)
