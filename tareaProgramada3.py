


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
                controladorLlenadoMasivo()
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
              width=30, height=2).pack(pady=5)
    # Ver estacionamiento
    marcoVer = tk.LabelFrame(ventana, text="2. Ver estacionamiento", padx=10, pady=5)
    marcoVer.pack(pady=5, padx=20, fill="x")
    tk.Button(marcoVer, text="a. Observar espacio",
            width=28,
            command=lambda: verEstacionamiento(config.obtenerTamanno(), config.obtenerListaObjetos())
            ).pack(pady=3)
    tk.Button(marcoVer, text="b. Estacionar un vehiculo",
            width=28).pack(pady=3)
    # Reportes 
    marcoReportes = tk.LabelFrame(ventana, text="3. Reportes", padx=10, pady=5)
    marcoReportes.pack(pady=5, padx=20, fill="x")
    tk.Button(marcoReportes, text="a. Cierre diario",               width=28).pack(pady=3)
    tk.Button(marcoReportes, text="b. Cierre por tipo de pago",     width=28).pack(pady=3)
    tk.Button(marcoReportes, text="c. Exportar cierre diario a CSV", width=28).pack(pady=3)
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


# programa principal
raiz = tk.Tk()
raiz.withdraw()
raiz.overrideredirect(True) 
controladorArranque()
raiz.mainloop()