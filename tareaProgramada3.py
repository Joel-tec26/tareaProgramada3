


import tkinter as tk
from tkinter import messagebox
from funionesJoel import *
from funcionesAlexiscopy import verEstacionamiento, observarEspacio
from manejoArchivos import *
from clase import Configuracion

config = Configuracion(
    tamanno         = 0,
    montoPorHora   = 0,
    tiempoGracia   = 0,
    tieneElectrico = False,
    listaObjetos   = []
)

def controladorArranque():
    """
    Funcionalidad:
        Verifica si existe una base de datos en memoria secundaria.
        Si existe la carga, si no abre la ventana de configuracion inicial.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    if existeConfiguracion():
        configCargado = cargarConfiguracion()
        config.asignarTamanno(configCargado.obtenerTamanno())
        config.asignarMontoPorHora(configCargado.obtenerMontoPorHora())
        config.asignarTiempoGracia(configCargado.obtenerTiempoGracia())
        config.asignarTieneElectrico(configCargado.obtenerTieneElectrico())
        config.asignarListaObjetos(cargarBaseDatos())
        abrirVentanaPrincipal()
    else:
        abrirVentanaConfiguracion(esInicial=True)


def controladorLlenadoMasivo():
    """
    Funcionalidad:
        Calcula el tope maximo masivo, carga el JSON, construye el diccionario,
        convierte a objetos, guarda la BD y abre la ventana principal.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    espaciosEspeciales  = max(2, int(config.obtenerTamanno() * 0.05))
    espaciosDisponibles = config.obtenerTamanno() - espaciosEspeciales
    if config.obtenerTieneElectrico():
        espaciosDisponibles -= 1
    topeMaximoMasivo = espaciosDisponibles - int(espaciosDisponibles * 0.05)

    datosJson   = cargarJson()
    diccionario = construirDiccionarioRestringido(datosJson, topeMaximoMasivo, config.obtenerMontoPorHora())

    print("\n Diccionario")
    for placa in diccionario:
        print(f"  {placa}: {diccionario[placa]}")

    config.listaObjetos = convertirDiccionarioAObjetos(diccionario)
    guardarBaseDatos(config.listaObjetos)
    print(f"base de tados guardada con {len(config.listaObjetos)} objetos.")
    print(f"Tamaño configurado: {config.obtenerTamanno()}")
    print(f"Lista objetos: {len(config.obtenerListaObjetos())}")
    abrirVentanaPrincipal()


def controladorGuardarConfiguracion(entradaTamanno, entradaMonto, entradaGracia,
                                     varElectrico, ventana, esInicial):
    """
    Funcionalidad:
        Valida y guarda los datos de configuracion ingresados por el usuario.
        Si es la configuracion inicial lanza el llenado masivo.
    Entrada:
        - entradaTamanno (Entry): Campo del tamaño del estacionamiento.
        - entradaMonto (Entry): Campo del monto por hora.
        - entradaGracia (Entry): Campo del tiempo de gracia.
        - varElectrico (BooleanVar): Variable del checkbox de electrico.
        - ventana (Toplevel): Ventana de configuracion.
        - esInicial (bool): True si es la primera configuracion.
    Salida:
        - (None)
    """
    valorTamanno = entradaTamanno.get()
    valorMonto  = entradaMonto.get()
    valorGracia = entradaGracia.get()

    if not valorTamanno.isdigit() or not valorMonto.isdigit() or not valorGracia.isdigit():
        messagebox.showerror("Error", "Todos los campos deben ser numeros enteros.")
        return
    confirmacion = messagebox.askyesno("Confirmar",
        f"Tamaño: {valorTamanno}\nMonto/hora: {valorMonto}\n"
        f"Gracia: {valorGracia} min\nElectrico: {'Si' if varElectrico.get() else 'No'}\n\n"
        f"Confirmar configuracion?")
    if confirmacion:
        config.asignarTamanno(int(valorTamanno))
        config.asignarMontoPorHora(int(valorMonto))
        config.asignarTiempoGracia(int(valorGracia))
        config.asignarTieneElectrico(varElectrico.get())
        guardarConfiguracion(config)
        ventana.destroy()
        if esInicial:
            listaVacia = crearListaVacia(config)
            config.asignarListaObjetos(listaVacia)
            guardarBaseDatos(config.obtenerListaObjetos())
            abrirVentanaPrincipal()
        else:
            messagebox.showinfo("Exito", "Configuracion actualizada correctamente.")


def abrirVentanaPrincipal():
    """
    Funcionalidad:
        Abre la ventana principal con el menu de botones del sistema
        organizado segun la especificacion.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Sistema de Estacionamiento")
    ventana.resizable(False, False)
    tk.Label(ventana, text="Sistema de Estacionamiento",
             font=("Arial", 16, "bold")).pack(pady=15)
    # Obtener vehiculos
    tk.Button(ventana, text="1. Obtener vehiculos",
          width=30, height=2,
          command=lambda: controladorLlenadoMasivo()# uso lambda para poder pasar parametros a la funcion del comando, sin lambda tkinter ejecutaria 
        #la funcion al momento de crear el boton y no cuando el usuario haga clic
          ).pack(pady=5)
    # Ver estacionamiento
    marcoVer = tk.LabelFrame(ventana, text="2. Ver estacionamiento", padx=10, pady=5)
    marcoVer.pack(pady=5, padx=20, fill="x")
    tk.Button(marcoVer, text="a. Observar espacio",
          width=28,
          command=lambda: verEstacionamiento(config.obtenerTamanno(), config.obtenerListaObjetos(), config)
          ).pack(pady=3)
    tk.Button(marcoVer, text="b. Estacionar un vehiculo",
          width=28,
          command=lambda: abrirSeleccionEspacio()
          ).pack(pady=3)
    # Reportes 
    marcoReportes = tk.LabelFrame(ventana, text="3. Reportes", padx=10, pady=5)
    marcoReportes.pack(pady=5, padx=20, fill="x")
    tk.Button(marcoReportes, text="a. Cierre diario",
          width=28,
          command=controladorCierreDiario).pack(pady=3)
    tk.Button(marcoReportes, text="b. Cierre por tipo de pago",     width=28).pack(pady=3)
    tk.Button(marcoReportes, text="c. Exportar cierre diario a CSV",
          width=28,
          command=controladorExportarCSV).pack(pady=3)
    # Configuracion 
    marcoConfig = tk.LabelFrame(ventana, text="4. Configuracion", padx=10, pady=5)
    marcoConfig.pack(pady=5, padx=20, fill="x")
    tk.Button(marcoConfig, text="a. Tamanno del estacionamiento",  width=28).pack(pady=3)
    tk.Button(marcoConfig, text="b. Tiempo de gracia en minutos",  width=28).pack(pady=3)
    tk.Button(marcoConfig, text="c. Modificar monto por hora",     width=28).pack(pady=3)
    #Acerca de 
    tk.Button(ventana, text="5. Acerca de",
              width=30, height=2).pack(pady=5)


# configuracion

def abrirVentanaConfiguracion(esInicial=False):
    """
    Funcionalidad:
        Abre la ventana de configuracion completa del estacionamiento.
    Entrada:
        - esInicial (bool): True si es la primera configuracion del sistema.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Configuracion")
    ventana.resizable(False, False)

    tk.Label(ventana, text="Configuracion del Estacionamiento",
             font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(ventana, text="Tamaño del estacionamiento:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entradaTamano = tk.Entry(ventana)
    entradaTamano.grid(row=1, column=1, padx=10)
    if not esInicial:
        entradaTamano.insert(0, str(config.obtenerTamanno()))

    tk.Label(ventana, text="Monto por hora (colones):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
    entradaMonto = tk.Entry(ventana)
    entradaMonto.grid(row=2, column=1, padx=10)
    if not esInicial:
        entradaMonto.insert(0, str(config.obtenerMontoPorHora()))

    tk.Label(ventana, text="Tiempo de gracia (minutos):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
    entradaGracia = tk.Entry(ventana)
    entradaGracia.grid(row=3, column=1, padx=10)
    if not esInicial:
        entradaGracia.insert(0, str(config.obtenerTiempoGracia()))

    varElectrico = tk.BooleanVar(value=config.obtenerTieneElectrico())
    tk.Checkbutton(ventana, text="Tiene espacio electrico?",
                   variable=varElectrico).grid(row=4, column=0, columnspan=2, pady=5)

    tk.Button(ventana, text="Guardar",
              command=lambda: controladorGuardarConfiguracion( 
                  entradaTamano, entradaMonto, entradaGracia,
                  varElectrico, ventana, esInicial)
              ).grid(row=5, column=0, pady=10)
    tk.Button(ventana, text="Regresar",
              command=ventana.destroy).grid(row=5, column=1, pady=10)

    if esInicial:
        ventana.grab_set()
        ventana.wait_window()

def controladorLlenadoMasivo():
    """
    Funcionalidad:
        Solicita al usuario la cantidad de vehiculos a asignar,
        los asigna aleatoriamente en espacios libres, genera vouchers
        y guarda la BD.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    ocupados         = calcularEspaciosOcupados(config.obtenerListaObjetos())
    topeMaximoMasivo = calcularEspaciosDisponibles(config)
    espaciosLibres   = topeMaximoMasivo - ocupados
    if espaciosLibres <= 0:
        messagebox.showwarning("Aviso", "No hay espacios disponibles para asignar vehiculos.")
        return
    ventana = tk.Toplevel()
    ventana.title("Obtener vehiculos")
    ventana.resizable(False, False)
    tk.Label(ventana, text=f"Campos disponibles: {espaciosLibres}",
             font=("Arial", 11)).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
    tk.Label(ventana, text="Cuantos vehiculos desea asignar:",
             font=("Arial", 11)).grid(row=1, column=0, padx=10, pady=5)
    entradaCantidad = tk.Entry(ventana)
    entradaCantidad.grid(row=1, column=1, padx=10)
    def confirmar():
        valor = entradaCantidad.get()
        if not valor.isdigit():
            messagebox.showerror("Error", "Ingrese un numero entero valido.")
            return
        cantidad = int(valor)
        if cantidad <= 0 or cantidad > espaciosLibres:
            messagebox.showerror("Error", f"Ingrese un numero entre 1 y {espaciosLibres}.")
            return
        ventana.destroy()
        datosJson    = cargarJson()
        listaObjetos = asignarVehiculosMasivos(config, datosJson, config.obtenerMontoPorHora(), cantidad)
        config.asignarListaObjetos(listaObjetos)
        generarVouchersLlenadoMasivo(config.obtenerListaObjetos(), config)
        guardarBaseDatos(config.obtenerListaObjetos())
        guardarConfiguracion(config)
        messagebox.showinfo("Exito", f"{cantidad} vehiculos asignados y vouchers generados.")
    tk.Button(ventana, text="Confirmar", command=confirmar).grid(row=2, column=0, pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).grid(row=2, column=1, pady=10)

# estacionar 1 vehiculo 
def abrirSeleccionEspacio():
    """
    Funcionalidad:
        Abre una ventana para que el usuario seleccione un espacio libre
        cuando estaciona desde el menu principal sin pasar por el mapa.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    ubicacionesLibres = obtenerUbicacionesLibres(config.obtenerListaObjetos(), config)
    if len(ubicacionesLibres) == 0:
        messagebox.showwarning("Aviso", "No hay espacios libres disponibles.")
        return
    ventana = tk.Toplevel()
    ventana.title("Seleccionar espacio")
    ventana.resizable(False, False)
    tk.Label(ventana, text="Seleccione un espacio libre:",
             font=("Arial", 11)).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
    numerosLibres = []
    for indice in ubicacionesLibres:
        numerosLibres.append(str(indice + 1))
    espacioVar = tk.StringVar(value=numerosLibres[0])
    tk.OptionMenu(ventana, espacioVar, *numerosLibres).grid(row=1, column=0, columnspan=2, pady=5)
    def confirmar():
        num = int(espacioVar.get())
        ventana.destroy()
        estacionarVehiculo(config.obtenerListaObjetos(), config, num, ventana)
    tk.Button(ventana, text="Continuar", command=confirmar).grid(row=2, column=0, pady=10)
    tk.Button(ventana, text="Cancelar",  command=ventana.destroy).grid(row=2, column=1, pady=10)

# cierre diario

def controladorCierreDiario():
    """
    Funcionalidad:
        Procesa todos los parqueos pendientes de pago, genera sus facturas,
        confecciona el reporte de cierre diario y guarda la BD actualizada.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    confirmacion = messagebox.askyesno("Confirmar",
        "Se procesaran todos los parqueos pendientes de pago.\n"
        "Se generaran facturas automaticas y el reporte del dia.\n\n"
        "Desea continuar?")
    if not confirmacion:
        return
    listaObjetos = procesarPendientes(config.obtenerListaObjetos(), config)
    config.asignarListaObjetos(listaObjetos)
    generarReporteCierreDiario(config.obtenerListaObjetos(), config)
    guardarBaseDatos(config.obtenerListaObjetos())
    guardarConfiguracion(config)
    messagebox.showinfo("Exito",
        "Cierre diario completado.\n"
        "Facturas generadas en carpeta 'facturas'.\n"
        "Reporte generado en carpeta 'reportes'.")

#exportar csv
def controladorExportarCSV():
    """
    Funcionalidad:
        Exporta el cierre diario a un archivo CSV sin titulos
        para ser abierto en Excel.
    Entrada:
        - (None)
    Salida:
        - (None)
    """
    exportarCierreDiarioCSV(config.obtenerListaObjetos())
    messagebox.showinfo("Exito",
        "Cierre diario exportado correctamente.\n"
        "Archivo guardado en carpeta 'reportes'.")
    


# programa principal
raiz = tk.Tk()
raiz.withdraw()
raiz.overrideredirect(True) 
controladorArranque()
raiz.mainloop()