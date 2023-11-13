from customtkinter import CTk


class ParentWindow(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("900x600+400+100")
        self.title("BeautyDataBase")
        self.resizable(False, False)
