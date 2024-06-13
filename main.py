# main.py



import tkinter as tk
from ui import LentesApp
from lentes_project.sistema_lentes import SistemaLentes

if __name__ == "__main__":
    root = tk.Tk()
    app = LentesApp(root)
    root.mainloop()
