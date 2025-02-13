import tkinter as tk
from tkinter import ttk

def configure_treeview_style(window):
    style = ttk.Style(window)  # Tk 인스턴스를 넘겨줘야 함
    style.configure("Treeview", font=("Arial", 20, "bold"), rowheight=60, background="#F0F0F0", fieldbackground="#F0F0F0")
    style.configure("Treeview.Heading", font=("Arial", 30, "bold"), padding=[40, 20, 40, 20])