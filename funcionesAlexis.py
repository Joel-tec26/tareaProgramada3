from funionesJoel import *
import tkinter as tk
from tkinter import ttk
import pickle
import datetime



def verEstacionamiento(tamaño, baseDatos, config):
    """
    """
    print("a")
    ventana = tk.Toplevel()
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
    def observarEspacio(baseDatos, num, valor, config):
        verEspacio = tk.Tk()
        verEspacio.title(f"Estacionamiento: {num}")
        verEspacio.geometry("300x300")
        def opcionesPago():
            menupago1 = tk.Tk()
            menupago1.title(f"Seleccion de tipo de pago")
            menupago1.geometry("400x150")
            tk.Label(menupago1, text=f"Tipo de Pago", font=("Arial", 20, "bold")).grid(row=0, column=0, padx=10, pady=5)
            tk.Label(menupago1,text="Seleccione el tipo de pago: ").grid(row=1, column=0, padx=10, pady=5)
            tipoPago=ttk.Combobox(menupago1, values=["Efectivo","Sinpe","Targeta"],state="readonly")
            tipoPago.grid(row=1,column=1)
            tipoPago.current(0)
            tk.Button(menupago1, text="Pagar", width=8, height=3, cursor="hand2", command=lambda:pagar()).grid(row=5, column=1, padx=10, pady=5)
            def pagar():
                def cerrarPestannas():
                    verEspacio.destroy()
                    menupago1.destroy()
                    menupago2.destroy()
                    generarUI(baseDatos,pagina=0)
                menupago2 = tk.Tk()
                menupago2.title(f"pago")
                menupago2.geometry("250x100")
                seleccion = tipoPago.get()
                if seleccion=="Efectivo":
                    opcion=1
                elif seleccion=="Sinpe":
                    opcion=2
                elif seleccion=="Targeta":
                    opcion=3
                baseDatos[num-1].asignarEstadia([baseDatos[num-1].obtenerEstadia()[0],baseDatos[num-1].obtenerEstadia()[1],datetime.datetime.now().strftime("%d/%m/%Y %H:%M")])
                baseDatos[num-1].asignarPago((baseDatos[num-1].obtenerPago()[0],opcion))
                generarVoucher(baseDatos[num-1],config)
                tk.Label(menupago2, text=f"Pago realizado con exito", font=("Arial", 10, "bold")).grid(padx=40)
                tk.Button(menupago2, text="click para regresar", width=14, height=2, cursor="hand2", command=cerrarPestannas).grid(row=1, column=0, padx=30, pady=5)
            menupago1.mainloop()
        if not valor:
            tk.Label(verEspacio, text=f"Campo: {num}", font=("Arial", 20, "bold")).grid(row=0, column=2, padx=0, pady=5)
            tk.Label(verEspacio, text="Placa: ", font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
            tk.Entry(verEspacio, font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=2)
            tk.Label(verEspacio, text="Marca: ", font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)
            tk.Entry(verEspacio, font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=2)
            tk.Label(verEspacio, text="Color: ", font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5)
            tk.Entry(verEspacio, font=("Arial", 10)).grid(row=3, column=2, padx=5, pady=2)
            tk.Label(verEspacio, text="Hora Entrada: ", font=("Arial", 10)).grid(row=4, column=1, padx=10, pady=5)
            tk.Entry(verEspacio, font=("Arial", 10)).grid(row=4, column=2, padx=5, pady=2)
            tk.Button(verEspacio, text="Estacionar", font=("Arial", 10, "bold"), width=8, height=3, bg="#B6CAFF", bd=0, activebackground="#B9C0FF", cursor="hand2", activeforeground="#ffffff").grid(row=5, column=1, padx=10, pady=5)
        else:
            tk.Label(verEspacio, text=f"Campo: {num}", font=("Arial", 20, "bold")).grid(row=0, column=2, padx=10, pady=5)
            tk.Label(verEspacio, text="Placa: ", font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
            tk.Label(verEspacio, text=f"{baseDatos[num-1].obtenerInfo()[0]}",font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=2)
            tk.Label(verEspacio, text="Marca: ", font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)
            tk.Label(verEspacio, text=f"{marcasValidas[baseDatos[num-1].obtenerInfo()[1]]}", font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=2)
            tk.Label(verEspacio, text="Color: ", font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5)
            tk.Label(verEspacio, text=f"{coloresValidos[baseDatos[num-1].obtenerInfo()[2]]}", font=("Arial", 10)).grid(row=3, column=2, padx=5, pady=2)
            tk.Label(verEspacio, text="Hora Entrada: ", font=("Arial", 10)).grid(row=4, column=1, padx=10, pady=5)
            tk.Label(verEspacio, text=f"{baseDatos[num-1].obtenerEstadia()[1]}",font=("Arial", 10)).grid(row=4, column=2, padx=5, pady=2)
            tk.Button(verEspacio, text="Pagar",font=("Arial", 10, "bold"), width=8, height=3,bg="#B6CAFF", bd=0, activebackground="#B9C0FF", cursor="hand2", command=lambda: opcionesPago(), activeforeground="#ffffff").grid(row=5, column=1, padx=10, pady=5)
        tk.Button(verEspacio, text="Regresar", font=("Arial", 10, "bold"),width=8, height=3, bg="#B6CAFF", bd=0,command=lambda: ventana.destroy(), activebackground="#B9C0FF", cursor="hand2", activeforeground="#ffffff").grid(row=5, column=2, padx=10, pady=5)
        verEspacio.mainloop()
        return
    def generarUI(baseDatos, pagina=0):
        #lo que hago acá, es borrar widgets ya que c
        for widget in marcoEstacionamientos.winfo_children():
            widget.destroy()
        for i in range(2):
            for o in range(1,9):
                indice=o+i*8+pagina*16
                bandera=False
                if indice==tamaño:
                    break
                for carro in baseDatos:
                    if int(carro.obtenerEstadia()[0]) == indice and carro.obtenerInfo()[0] != "" and carro.obtenerEstadia()[2]=="":
                        bandera = True
                borde = tk.Frame(marcoEstacionamientos, bg="#FF6E6E" if bandera else "#79FF96", padx=5, pady=5)
                borde.grid(row=i,column=o,padx=10,pady=80)
                #uso lambda porque es la unica forma de pasar parametros en en command, sin este, el comando se ejecuta solo y usar el boton no serviria
                #ademas, asigno variables en el lambda para que cada boton tenga parametros unicos y no el mismo por ser generados en for
                tk.Button(borde, text=f"{indice}", font=("Arial", 30, "bold"), width=3, height=3, bg="#FF5959" if bandera else "#59FF7D", fg="#ffffff", bd=0, command=lambda indice=indice, bandera=bandera: observarEspacio(baseDatos, indice,valor=bandera, config=config), activebackground="#FF3F4F" if bandera else "#2EFF74", cursor="hand2").grid()
            if indice+1>=tamaño:
                if 16>=tamaño:
                    if 8>=tamaño and i==0:
                        break
                    if i==1:
                        break
                borde = tk.Frame(marcoEstacionamientos, bg="#C2D2FF", padx=5, pady=5)
                borde.grid(row=0,column=9,padx=80,pady=80, sticky="e")
                tk.Button(borde, text="Anterior", font=("Arial", 10, "bold"),width=8, height=5, bg="#B6CAFF", bd=0, command=lambda pagina=pagina:CambiarPagina(baseDatos, modo=1,pagina=pagina) , activebackground="#B9C0FF", cursor="hand2", activeforeground="#ffffff").grid()
                break
            elif pagina==0:
                if 16>=tamaño:
                    if 8>=tamaño and i==0:
                        break
                    if i==1:
                        break
                borde = tk.Frame(marcoEstacionamientos, bg="#C2D2FF", padx=5, pady=5)
                borde.grid(row=0,column=9,padx=80,pady=80, sticky="e")
                tk.Button(borde, text="Siguente", font=("Arial", 10, "bold"),width=8, height=5, bg="#B6CAFF", bd=0, command=lambda pagina=pagina:CambiarPagina(baseDatos,modo=0, pagina=pagina), activebackground="#B9C0FF", cursor="hand2", activeforeground="#ffffff").grid()
            else:
                borde = tk.Frame(marcoEstacionamientos, bg="#C2D2FF", padx=5, pady=5)
                borde.grid(row=i,column=9,padx=80,pady=80)
                tk.Button(borde, text="Siguente" if i==0 else "Anterior", font=("Arial", 10, "bold"),width=8, height=5, bg="#B6CAFF", bd=0, command=lambda i=i, pagina=pagina:CambiarPagina(baseDatos,modo=0, pagina=pagina) if i==0 else CambiarPagina(baseDatos, modo=1,pagina=pagina) , activebackground="#B9C0FF", cursor="hand2", activeforeground="#ffffff").grid()
    generarUI(baseDatos)


def asignarInfo(baseDatos,tipo):
    xml=""
    for carro in baseDatos:
        print(carro.obtenerPago()[1])
        if carro.obtenerPago()[1]==tipo:
            xml+=f"\t\t<carro>\n"
            xml+=f"\t\t\t<placa>{carro.obtenerInfo()[0]}</placa>\n"
            xml+=f"\t\t\t<marca>{carro.obtenerInfo()[1]}</marca>\n"
            xml+=f"\t\t\t<color>{carro.obtenerInfo()[2]}</color>\n"
            xml+=f"\t\t\t<tipo>{carro.obtenerInfo()[3]}</tipo>\n"
            xml+=f"\t\t\t<ubicacion>{carro.obtenerEstadia()[0]}</ubicacion>\n"
            xml+=f"\t\t\t<fechaHoraEntrada>{carro.obtenerEstadia()[1]}</fechaHoraEntrada>\n"
            xml+=f"\t\t\t<fechaHoraSalida>{carro.obtenerEstadia()[2]}</fechaHoraSalida>\n"
            xml+=f"\t\t</carro>\n"
    return xml

def generarReporteTipoPago(baseDatos):
    efectivo=asignarInfo(baseDatos,1)
    sinpe=asignarInfo(baseDatos,2)
    targeta=asignarInfo(baseDatos,3)
    xml="<reporte>\n"
    xml+="\t<efectivo>\n"
    xml+=efectivo
    xml+="\t</efectivo>\n"
    xml+="\t<sinpe>\n"
    xml+=sinpe
    xml+="\t<sinpe>\n"
    xml+="\t<targeta>\n"
    xml+=targeta
    xml+="\t</targeta>\n"
    xml+="</reporte>"
    archivo = open(f"Reporte-Por-Tipo-De-Pago.xml","w")
    archivo.write(xml)
    return