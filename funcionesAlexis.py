from funcionesAlexis import *
import tkinter as tk
from tkinter import messagebox, ttk

baseDatos=[] #prueba

for i in range(70):
    baseDatos.append([])

def observarEspacio(baseDatos, num):
    return

def verEstacionamiento(baseDatos):
    """
    """
    ventana = tk.Tk()
    ventana.title("Insertar donador")
    ventana.geometry("1020x720")
    ventana.grid_columnconfigure(1, weight=1)
    tk.Label(ventana, text="Ver Estacionamiento", font=("Arial", 20)).grid(row=0, column=1, padx=10, pady=5)
    marcoBotones = tk.Frame(ventana)
    marcoBotones.grid(row=1, column=0, columnspan=3, sticky="w")
    pagina=0
    def generarUI(baseDatos, pagina):
        for i in range(2):
            for o in range(8):
                indice=o+i*8+pagina*16
                borde = tk.Frame(marcoBotones, bg="#FF6E6E" if baseDatos[indice] else "#6EFF8E", padx=5, pady=5)
                borde.grid(row=i,column=o,padx=10,pady=80)
                tk.Button(borde, text="", width=10, height=10, bg="#FF5959" if baseDatos[indice] else "#59FF7D", bd=0, command=lambda i=i, o=o: observarEspacio(baseDatos, indice), activebackground="#FF3F4F" if baseDatos[indice] else "#2EFF74").grid()
    generarUI(baseDatos, pagina)
    ventana.mainloop()