from funcionesAlexis import *
import tkinter as tk
from tkinter import messagebox, ttk

baseDatos=[]

for i in range(15):
    baseDatos.append([])

def observarEspacio(baseDatos, num):
    ventana = tk.Tk()
    ventana.title("Estacionamiento: asdasd") #CAMBIAR
    ventana.geometry("400x500")
    if not baseDatos[num]:
        tk.Label(ventana, text="Campo: asdas", font=("Arial", 20, "bold")).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(ventana, text="Placa: ", font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
        tk.Entry(ventana, font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Marca: ", font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)
        tk.Entry(ventana, font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Color: ", font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5)
        tk.Entry(ventana, font=("Arial", 10)).grid(row=3, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Hora Entrada: ", font=("Arial", 10)).grid(row=4, column=1, padx=10, pady=5)
        tk.Entry(ventana, font=("Arial", 10)).grid(row=4, column=2, padx=5, pady=2)
        tk.Button(ventana, text="Pagar", width=8, height=4, bg="#B3F0FF", bd=0, activebackground="#B3DDFF", cursor="hand2").grid(row=5, column=1, padx=10, pady=5)
        tk.Button(ventana, text="Regresar", width=8, height=4, bg="#B3F0FF", bd=0, activebackground="#B3DDFF", cursor="hand2").grid(row=5, column=2, padx=10, pady=5)
    else:
        tk.Label(ventana, text="Campo: asdas", font=("Arial", 20)).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(ventana, text="Placa: ", font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
        tk.Label(ventana, text="ASD",font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Marca: ", font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)
        tk.Label(ventana, text="ASD",font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Color: ", font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5)
        tk.Label(ventana, text="ASD",font=("Arial", 10)).grid(row=3, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Hora Entrada: ", font=("Arial", 10)).grid(row=4, column=1, padx=10, pady=5)
        tk.Label(ventana, text="ASD",font=("Arial", 10)).grid(row=4, column=2, padx=5, pady=2)
        tk.Button(ventana, text="Estacionar", width=8, height=4, bg="#B3F0FF", bd=0, activebackground="#B3DDFF", cursor="hand2").grid(row=5, column=1, padx=10, pady=5)
        tk.Button(ventana, text="Regresar", width=8, height=4, bg="#B3F0FF", bd=0, activebackground="#B3DDFF", cursor="hand2").grid(row=5, column=2, padx=10, pady=5)
    return

def verEstacionamiento(baseDatos):
    """
    """
    ventana = tk.Tk()
    ventana.title("Estacionamiento")
    ventana.geometry("1020x720")
    tk.Label(ventana, text="Ver Estacionamiento", font=("Arial", 20, "bold")).grid(row=0, column=1, padx=10, pady=5)
    marcoEstacionamientos = tk.Frame(ventana)
    marcoEstacionamientos.grid(row=1, column=0, columnspan=3, sticky="w")
    def CambiarPagina(baseDatos, modo, pagina):
        """
        Funcionamiento: cambia de pagina dependiendo de que modo se use: 0 para ir a la siguiente pagina, 1 para ir a la anterior
        """
        if modo==0:
            generarUI(baseDatos,pagina+1)
            return pagina+1
        elif modo==1:
            generarUI(baseDatos,pagina-1)
            return pagina-1
        print("Error al tratar de llamar esta funcion, uso de modo incorrecto")
    def generarUI(baseDatos, pagina=0):
        for widget in marcoEstacionamientos.winfo_children():
            widget.destroy()
        for i in range(2):
            for o in range(8):
                indice=o+i*8+pagina*16
                if indice>=len(baseDatos):
                    break
                borde = tk.Frame(marcoEstacionamientos, bg="#FF6E6E" if baseDatos[indice] else "#79FF96", padx=5, pady=5)
                borde.grid(row=i,column=o,padx=10,pady=80)
                tk.Button(borde, text="", width=10, height=10, bg="#FF5959" if baseDatos[indice] else "#59FF7D", bd=0, command=lambda indice=indice: observarEspacio(baseDatos, indice), activebackground="#FF3F4F" if baseDatos[indice] else "#2EFF74", cursor="hand2").grid()
            if indice+1>=len(baseDatos):
                if 16>=len(baseDatos):
                    if 8>=len(baseDatos) and i==0:
                        break
                    if i==1:
                        break
                borde = tk.Frame(marcoEstacionamientos, bg="#E5FFFE", padx=5, pady=5)
                borde.grid(row=0,column=8,padx=80,pady=80, sticky="e")
                tk.Button(borde, text="Anterior", width=8, height=5, bg="#B6FFFB", bd=0, command=lambda pagina=pagina:CambiarPagina(baseDatos, modo=1,pagina=pagina) , activebackground="#B3F0FF", cursor="hand2").grid()
                break
            elif pagina==0:
                if 16>=len(baseDatos):
                    if 8>=len(baseDatos) and i==0:
                        break
                    if i==1:
                        break
                borde = tk.Frame(marcoEstacionamientos, bg="#E5FFFE", padx=5, pady=5)
                borde.grid(row=0,column=8,padx=80,pady=80, sticky="e")
                tk.Button(borde, text="Siguente", width=8, height=5, bg="#B6FFFB", bd=0, command=lambda pagina=pagina:CambiarPagina(baseDatos,modo=0, pagina=pagina), activebackground="#B3F0FF", cursor="hand2").grid()
            else:
                borde = tk.Frame(marcoEstacionamientos, bg="#E5FFFE", padx=5, pady=5)
                borde.grid(row=i,column=8,padx=80,pady=80)
                tk.Button(borde, text="Siguente" if i==0 else "Anterior", width=8, height=5, bg="#B6FFFB", bd=0, command=lambda i=i, pagina=pagina:CambiarPagina(baseDatos,modo=0, pagina=pagina) if i==0 else CambiarPagina(baseDatos, modo=1,pagina=pagina) , activebackground="#B3F0FF", cursor="hand2").grid()
    generarUI(baseDatos)
    ventana.mainloop()

baseDatos[0]=1
verEstacionamiento(baseDatos)