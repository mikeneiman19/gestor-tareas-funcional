import ttkbootstrap as ttk
from interfaz import TareasApp

if __name__ == "__main__":
    ventana = ttk.Window(themename="superhero")
    TareasApp(ventana)
    ventana.mainloop()