import customtkinter as CTk

from windows.start_main_windows import StartWindow

CTk.set_appearance_mode("light")  # Modes: system (default), light, dark
CTk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

if __name__ == "__main__":
    StartWindow().mainloop()
