import tkinter as tk
from google_GUI_Tkinter import App
import logging


if __name__ == '__main__':
    logging.basicConfig(filename='log_file.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    root = tk.Tk()
    app = App(root)
    root.mainloop()

