from os import listdir
import customtkinter as CTk
import tkinter


class CreateDatabaseWindow(CTk.CTkToplevel):
    def __init__(self, databases_optional_menu):
        super().__init__()

        self.databases_optional_menu = databases_optional_menu

        # Настройки
        self.geometry("400x250+700+250")
        self.title("BeautyDataBase")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss(self))  # перехватываем нажатие на крестик

        # Ввод названия базы данных
        self.entry = CTk.CTkEntry(master=self, width=200)
        self.entry.place(relx=.5, rely=.43, anchor=tkinter.CENTER)

        # Кнопка создания новой базы данных
        self.create_database_button = CTk.CTkButton(master=self, text="Создать базу данных", width=200,
                                                    command=self.create_database)
        self.create_database_button.place(relx=.5, rely=.57, anchor=tkinter.CENTER)

        self.grab_set()  # захватываем пользовательский ввод

    def create_database(self):
        with open(f"databases/{self.entry.get()}.db", "w"):
            pass
        self.databases_optional_menu.configure(values=listdir("databases"))
        self.grab_release()
        self.destroy()

    # Нажатие на крестик
    @staticmethod
    def dismiss(window):
        window.grab_release()
        window.destroy()