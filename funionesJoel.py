# Creado por: Joel Porras y Alexis Torres
# Fecha de creación: 15/06/2026 7:16 am
# Ultima modificación: 15/06/2026 
# versión: 3.14

# importacion de librerias
import json
import random
from datetime import datetime, timedelta
from clase import Estacionamiento
import qrcode
import os
from manejoArchivos import guardarBaseDatos
import tkinter as tk
from tkinter import messagebox


"""
uso os para interactuar con el sistema de archivos en especifico
os.path.exists que verifica si la carpeta vouchers existe, os.makedirs que crea la carpeta vouchers si no existe, os.path.join que une rutas de 
forma compatible con cualquier sistema operativo. Pickle no puede realizar estas operaciones ya que solo sirve para serializar y guardar objetos Python en memoria secundaria
"""
from fpdf import FPDF

marcasValidas = ["Toyota", "Honda", "Hyundai", "Kia", "Nissan",
                  "Suzuki", "Mitsubishi", "Mazda", "Ford", "Chevrolet",
                  "Land Rover", "GMC", "Saturn"]

coloresValidos= ["Blanco", "Negro", "Rojo", "Azul", "Gris",
                   "Plata", "Verde", "Amarillo", "Café", "Naranja",
                   "Mauv", "Khaki", "Orange"]

tiposValidos = ["Sedan", "SUV", "Pickup", "Hatchback", "Van",
                 "Coupe", "Convertible"]

archivojson = "vehicle_data.json"


def cargarJson():
    """
    Funcionalidad:
        Lee el archivo vehicle_data.json del disco y retorna
        su contenido como lista de diccionarios.
    Entrada:
        - (None)
    Salida:
        - datosJson (list): Lista de registros crudos del archivo JSON.
    """
    archivo = open(archivojson, "r", encoding="utf-8")
    datosJson = json.load(archivo)
    archivo.close()
    return datosJson

def buscarIndiceEnLista(lista, valor):
    """
    Funcionalidad:
        Busca un valor en una lista y retorna su índice.
        Si no lo encuentra retorna -1.
    Entrada:
        - lista (list): Lista donde se busca el valor.
        - valor (str): Valor a buscar en la lista.
    Salida:
        - indice (int): Posición del valor en la lista, -1 si no existe.
    """
    indice = 0
    encontrado = False
    while indice < len(lista) and not encontrado:
        if lista[indice] == valor:
            encontrado = True
        else:
            indice += 1
    if encontrado:
        return indice
    return -1


def extraerPlaca(registro, indiceFallback):
    """
    Funcionalidad:
        Extrae la placa del campo vehicle_vin del registro.
        Si no existe genera una placa sintética con el índice.
    Entrada:
        - registro (dict): Registro crudo de un vehículo.
        - indiceFallback (int): Índice para generar placa si no viene en el JSON.
    Salida:
        - placa (str): Placa del vehículo.
    """
    if "vehicle_vin" in registro:
        return str(registro["vehicle_vin"])[:8]
    return f"error: {indiceFallback:04d}"


def extraerMarca(registro):
    """
    Funcionalidad:
        Extrae la marca del campo vehicle_make del registro.
        Si no viene o no está en la lista válida, asigna aleatoriamente.
    Entrada:
        - registro (dict): Registro crudo de un vehículo.
    Salida:
        - indice (int): Índice de la marca en marcasValidas.
    """
    if "vehicle_make" in registro:
        valorMarca = str(registro["vehicle_make"]).strip()
        indice = buscarIndiceEnLista(marcasValidas, valorMarca)
        if indice != -1:
            return indice
    return random.randint(0, len(marcasValidas) - 1)

def extraerColor(registro):
    """
    Funcionalidad:
        Extrae el color del campo color del registro.
        Si no viene o no está en la lista válida, asigna aleatoriamente.
    Entrada:
        - registro (dict): Registro crudo de un vehículo.
    Salida:
        - indice (int): Índice del color en coloresValidos.
    """
    if "color" in registro:
        valorColor = str(registro["color"]).strip()
        indice = buscarIndiceEnLista(coloresValidos, valorColor)
        if indice != -1:
            return indice
    return random.randint(0, len(coloresValidos) - 1)


def extraerTipo(registro):
    """
    Funcionalidad:
        Extrae el tipo de vehículo del campo chassis del registro.
        Si no viene o no está en la lista válida, asigna aleatoriamente.
    Entrada:
        - registro (dict): Registro crudo de un vehículo.
    Salida:
        - indice (int): Índice del tipo en tiposValidos.
    """
    if "chassis" in registro:
        valorTipo = str(registro["chassis"]).strip()
        indice = buscarIndiceEnLista(tiposValidos, valorTipo)
        if indice != -1:
            return indice
    return random.randint(0, len(tiposValidos) - 1)


def generarFechaEntradaAleatoria():
    """
    Funcionalidad:
        Genera una fecha y hora de entrada aleatoria entre las 7:00 am
        y las 9:00 pm del día actual.
    Entrada:
        - (None)
    Salida:
        - fechaHoraEntrada (str): Fecha y hora formateada como DD/MM/AAAA HH:mm.
    """
    horaApertura       = datetime.now().replace(hour=7,  minute=0, second=0, microsecond=0)
    horaCierre         = datetime.now().replace(hour=21, minute=0, second=0, microsecond=0)
    diferenciaSegundos = int((horaCierre - horaApertura).total_seconds())
    segundosAleatorios = random.randint(0, diferenciaSegundos)
    fechaHoraEntrada   = horaApertura + timedelta(seconds=segundosAleatorios)
    return fechaHoraEntrada.strftime("%d/%m/%Y %H:%M")


def construirDiccionarioRestringido(datosJson, cantidadVehiculos, montoPorHora):
    """
    Funcionalidad:
        Construye el diccionario con la cantidad indicada de vehiculos.
        Si el JSON tiene menos registros que la cantidad solicitada,
        genera datos aleatorios para completar.
    Entrada:
        - datosJson (list): Lista de registros crudos del archivo JSON.
        - cantidadVehiculos (int): Cantidad de vehiculos a procesar.
        - montoPorHora (int): Monto parametrizado para el cobro por hora.
    Salida:
        - diccionario (dict): Diccionario {placa: [marca, color, tipo, ubicacion,
                              fechaHoraEntrada, fechaHoraSalida, monto, tipoPago]}.
    """
    diccionario  = {}
    contador     = 1
    indiceJson   = 0
    while contador <= cantidadVehiculos:
        if indiceJson < len(datosJson):
            registro = datosJson[indiceJson]
            placa    = extraerPlaca(registro, contador)
            marca    = extraerMarca(registro)
            color    = extraerColor(registro)
            tipo     = extraerTipo(registro)
        else:
            placa = f"CR{contador:04d}"
            marca = random.randint(0, len(marcasValidas) - 1)
            color = random.randint(0, len(coloresValidos) - 1)
            tipo  = random.randint(0, len(tiposValidos) - 1)
        if placa in diccionario:
            placa = placa + str(contador)

        ubicacion        = str(contador)
        fechaHoraEntrada = generarFechaEntradaAleatoria()
        fechaHoraSalida  = ""
        monto            = montoPorHora
        tipoPago         = 0

        diccionario[placa] = [
            marca,             # [0]
            color,             # [1]
            tipo,              # [2]
            ubicacion,         # [3]
            fechaHoraEntrada,  # [4]
            fechaHoraSalida,   # [5]
            monto,             # [6]
            tipoPago           # [7]
        ]
        contador  += 1
        indiceJson += 1
    return diccionario


def convertirDiccionarioAObjetos(diccionario):
    """
    Funcionalidad:
        Recorre el diccionario restringido y crea un objeto Estacionamiento
        por cada entrada, retornando la lista de objetos.
    Entrada:
        - diccionario (dict): Diccionario {placa: [marca, color, tipo, ubicacion,
                              fechaHoraEntrada, fechaHoraSalida, monto, tipoPago]}.
    Salida:
        - listaObjetos (list): Lista de objetos Estacionamiento instanciados.
    """
    listaObjetos = []
    identificador = 1

    for placa in diccionario:
        datosVehiculo    = diccionario[placa]
        marca            = datosVehiculo[0]
        color            = datosVehiculo[1]
        tipo             = datosVehiculo[2]
        ubicacion        = datosVehiculo[3]
        fechaHoraEntrada = datosVehiculo[4]
        fechaHoraSalida  = datosVehiculo[5]
        monto            = datosVehiculo[6]
        tipoPago         = datosVehiculo[7]

        objetoEstacionamiento = Estacionamiento(
            identificador = str(identificador),
            info          = (placa, marca, color, tipo),
            estadia       = [ubicacion, fechaHoraEntrada, fechaHoraSalida],
            pago          = (monto, tipoPago)
        )
        listaObjetos.append(objetoEstacionamiento)
        identificador += 1

    return listaObjetos

# registro masivo

def calcularEspaciosDisponibles(config):
    """
    Funcionalidad:
        Calcula cuantos espacios generales estan disponibles para el llenado masivo
        respetando especiales, electrico y el 5% libre obligatorio.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - topeMaximoMasivo (int): Cantidad maxima de vehiculos a asignar masivamente.
    """
    espaciosEspeciales  = max(2, int(config.obtenerTamanno() * 0.05))
    espaciosDisponibles = config.obtenerTamanno() - espaciosEspeciales
    if config.obtenerTieneElectrico():
        espaciosDisponibles -= 1
    topeMaximoMasivo = espaciosDisponibles - int(espaciosDisponibles * 0.05)
    return topeMaximoMasivo

def calcularEspaciosOcupados(listaObjetos):
    """
    Funcionalidad:
        Cuenta cuantos espacios generales ya estan ocupados en la lista de objetos.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
    Salida:
        - ocupados (int): Cantidad de espacios con vehiculo asignado.
    """
    ocupados = 0
    for objeto in listaObjetos:
        if objeto.obtenerInfo()[0] != "":
            ocupados += 1
    return ocupados

def obtenerUbicacionesLibres(listaObjetos, config):
    """
    Funcionalidad:
        Retorna una lista con los indices de los espacios generales libres,
        excluyendo los especiales y el electrico.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - ubicacionesLibres (list): Lista de indices disponibles para asignar.
    """
    espaciosEspeciales = max(2, int(config.obtenerTamanno() * 0.05))
    inicioGenerales    = espaciosEspeciales
    if config.obtenerTieneElectrico():
        inicioGenerales += 1

    ubicacionesLibres = []
    indice = inicioGenerales
    while indice < len(listaObjetos):
        objeto = listaObjetos[indice]
        if objeto.obtenerInfo()[0] == "":
            ubicacionesLibres.append(indice)
        indice += 1
    return ubicacionesLibres

def asignarVehiculosMasivos(config, datosJson, montoPorHora, cantidadSolicitada):
    """
    Funcionalidad:
        Asigna la cantidad solicitada de vehiculos a espacios generales libres
        del parqueo, respetando el tope maximo masivo.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
        - datosJson (list): Lista de registros del archivo JSON.
        - montoPorHora (int): Monto parametrizado por hora.
        - cantidadSolicitada (int): Cantidad de vehiculos que el usuario quiere asignar.
    Salida:
        - listaObjetos (list): Lista de objetos actualizada con los nuevos vehiculos.
    """
    listaObjetos      = config.obtenerListaObjetos()
    topeMaximoMasivo  = calcularEspaciosDisponibles(config)
    ocupados          = calcularEspaciosOcupados(listaObjetos)
    espaciosALlenar   = topeMaximoMasivo - ocupados
    ubicacionesLibres = obtenerUbicacionesLibres(listaObjetos, config)
    if espaciosALlenar <= 0:
        print("No hay espacios disponibles para llenar masivamente.")
        return listaObjetos
    if cantidadSolicitada < espaciosALlenar:
        espaciosALlenar = cantidadSolicitada
    random.shuffle(ubicacionesLibres)
    diccionario = construirDiccionarioRestringido(datosJson, espaciosALlenar, montoPorHora)
    placas      = list(diccionario.keys())
    indiceVehiculo  = 0
    indiceUbicacion = 0
    while indiceVehiculo < len(placas) and indiceUbicacion < len(ubicacionesLibres):
        placa         = placas[indiceVehiculo]
        datosVehiculo = diccionario[placa]
        posicion      = ubicacionesLibres[indiceUbicacion]
        objeto        = listaObjetos[posicion]
        objeto.asignarInfo((placa, datosVehiculo[0], datosVehiculo[1], datosVehiculo[2]))
        objeto.asignarEstadia([str(posicion + 1), datosVehiculo[4], datosVehiculo[5]])
        objeto.asignarPago((datosVehiculo[6], datosVehiculo[7]))
        indiceVehiculo  += 1
        indiceUbicacion += 1
    return listaObjetos

def generarCodigoQR(placa, marca, tipo, fechaHoraEntrada, rutaQR):
    """
    Funcionalidad:
        Genera un codigo QR con la informacion del vehiculo y lo guarda en disco.
    Entrada:
        - placa (str): Placa del vehiculo.
        - marca (str): Marca del vehiculo en texto.
        - tipo (str): Tipo del vehiculo en texto.
        - fechaHoraEntrada (str): Fecha y hora de entrada del vehiculo.
        - rutaQR (str): Ruta donde se guarda la imagen del QR.
    Salida:
        - (None)
    """
    contenidoQR = f"{placa}-{marca}-{tipo}-{fechaHoraEntrada}"
    imagenQR    = qrcode.make(contenidoQR)
    imagenQR.save(rutaQR)


def generarVoucher(objeto, config):
    """
    Funcionalidad:
        Genera un voucher en PDF con la informacion del vehiculo estacionado
        y un codigo QR con los datos principales.
    Entrada:
        - objeto (Estacionamiento): Objeto con la informacion del vehiculo.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    placa            = objeto.obtenerInfo()[0]
    marcaIndice      = objeto.obtenerInfo()[1]
    colorIndice      = objeto.obtenerInfo()[2]
    tipoIndice       = objeto.obtenerInfo()[3]
    fechaHoraEntrada = objeto.obtenerEstadia()[1]
    ubicacion        = objeto.obtenerEstadia()[0]

    marca = marcasValidas[marcaIndice]
    color = coloresValidos[colorIndice]
    tipo  = tiposValidos[tipoIndice]

    fechaFormato = fechaHoraEntrada.replace("/", "-").replace(" ", "_").replace(":", "")
    nombrePdf    = f"voucher_{placa}_{fechaFormato}.pdf"
    nombreQR     = f"qr_{placa}_{fechaFormato}.png"
    if not os.path.exists("vouchers"):
        os.makedirs("vouchers")
    rutaPdf = os.path.join("vouchers", nombrePdf)
    rutaQR  = os.path.join("vouchers", nombreQR)
    generarCodigoQR(placa, marca, tipo, fechaHoraEntrada, rutaQR)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, "Voucher de Estacionamiento", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Informacion del vehiculo", ln=True)
    pdf.ln(3)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Placa          : {placa}",            ln=True)
    pdf.cell(0, 8, f"Marca          : {marca}",            ln=True)
    pdf.cell(0, 8, f"Color          : {color}",            ln=True)
    pdf.cell(0, 8, f"Tipo           : {tipo}",             ln=True)
    pdf.cell(0, 8, f"Ubicacion      : {ubicacion}",        ln=True)
    pdf.cell(0, 8, f"Hora entrada   : {fechaHoraEntrada}", ln=True)
    pdf.cell(0, 8, f"Monto por hora : {config.obtenerMontoPorHora()} colones", ln=True)
    pdf.image(rutaQR, x=140, y=40, w=60, h=60)
    pdf.output(rutaPdf)


def generarVouchersLlenadoMasivo(listaObjetos, config):
    """
    Funcionalidad:
        Recorre la lista de objetos y genera un voucher en PDF
        por cada vehiculo que tenga placa asignada.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    for objeto in listaObjetos:
        if objeto.obtenerInfo()[0] != "":
            generarVoucher(objeto, config)
    print("Vouchers generados en la carpeta 'vouchers'.")

def crearListaVacia(config):
    """
    Funcionalidad:
        Crea la lista de objetos Estacionamiento con todos los espacios
        vacios segun el tamanno configurado.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - listaObjetos (list): Lista de objetos Estacionamiento vacios.
    """
    listaObjetos = []
    contador     = 1
    while contador <= config.obtenerTamanno():
        objetoEstacionamiento = Estacionamiento(
            identificador = str(contador),
            info          = ("", 0, 0, 0),
            estadia       = [str(contador), "", ""],
            pago          = (0, 0)
        )
        listaObjetos.append(objetoEstacionamiento)
        contador += 1
    return listaObjetos

# estacionar 1 vehiculo 
def estacionarVehiculo(baseDatos, config, num, ventanaPadre):
    """
    Funcionalidad:
        Abre la ventana para registrar un vehiculo en un espacio libre.
        Solicita placa, marca, color y tipo, asigna la ubicacion y genera voucher.
    Entrada:
        - baseDatos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
        - num (int): Numero del espacio seleccionado.
        - ventanaPadre (Toplevel): Ventana padre para cerrarla al confirmar.
    Salida:
        - (None)
    """

    ventana = tk.Toplevel()
    ventana.title(f"Estacionar en espacio {num}")
    ventana.resizable(False, False)
    tk.Label(ventana, text=f"Espacio: {num}",
             font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
    tk.Label(ventana, text="Placa:", font=("Arial", 10)).grid(row=1, column=0, sticky="e", padx=10, pady=5)
    entradaPlaca = tk.Entry(ventana, font=("Arial", 10))
    entradaPlaca.grid(row=1, column=1, padx=10)
    tk.Label(ventana, text="Marca:", font=("Arial", 10)).grid(row=2, column=0, sticky="e", padx=10, pady=5)
    marcaVar = tk.StringVar(value=marcasValidas[0])
    tk.OptionMenu(ventana, marcaVar, *marcasValidas).grid(row=2, column=1, padx=10, sticky="w")
    tk.Label(ventana, text="Color:", font=("Arial", 10)).grid(row=3, column=0, sticky="e", padx=10, pady=5)
    colorVar = tk.StringVar(value=coloresValidos[0])
    tk.OptionMenu(ventana, colorVar, *coloresValidos).grid(row=3, column=1, padx=10, sticky="w")
    tk.Label(ventana, text="Tipo:", font=("Arial", 10)).grid(row=4, column=0, sticky="e", padx=10, pady=5)
    tipoVar = tk.StringVar(value=tiposValidos[0])
    tk.OptionMenu(ventana, tipoVar, *tiposValidos).grid(row=4, column=1, padx=10, sticky="w")
    horaEntrada = datetime.now().strftime("%d/%m/%Y %H:%M")
    tk.Label(ventana, text="Hora entrada:", font=("Arial", 10)).grid(row=5, column=0, sticky="e", padx=10, pady=5)
    entradaHora = tk.Entry(ventana, font=("Arial", 10))
    entradaHora.grid(row=5, column=1, padx=10)
    tk.Label(ventana, text="(DD/MM/AAAA HH:MM)", font=("Arial", 8), fg="gray").grid(row=6, column=1, sticky="w", padx=10)
    def confirmar():
        placa       = entradaPlaca.get().strip()
        horaEntrada = entradaHora.get().strip()
        if placa == "":
            messagebox.showerror("Error", "La placa no puede estar vacia.")
            return
        if horaEntrada == "":
            messagebox.showerror("Error", "La hora de entrada no puede estar vacia.")
            return
        try:
            datetime.strptime(horaEntrada, "%d/%m/%Y %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Formato de hora invalido. Use DD/MM/AAAA HH:MM")
            return
        for objeto in baseDatos:
            if objeto.obtenerInfo()[0] == placa:
                messagebox.showerror("Error", "Ya existe un vehiculo con esa placa.")
                return
        confirmacion = messagebox.askyesno("Confirmar",
            f"Placa   : {placa}\n"
            f"Marca   : {marcaVar.get()}\n"
            f"Color   : {colorVar.get()}\n"
            f"Tipo    : {tipoVar.get()}\n"
            f"Entrada : {horaEntrada}\n"
            f"Espacio : {num}\n\n"
            f"Confirmar estacionamiento?")
        if confirmacion:
            marcaIndice = buscarIndiceEnLista(marcasValidas, marcaVar.get())
            colorIndice = buscarIndiceEnLista(coloresValidos, colorVar.get())
            tipoIndice  = buscarIndiceEnLista(tiposValidos,  tipoVar.get())
            objeto = baseDatos[num - 1]
            objeto.asignarInfo((placa, marcaIndice, colorIndice, tipoIndice))
            objeto.asignarEstadia([str(num), horaEntrada, ""])
            objeto.asignarPago((0, 0))
            generarVoucher(objeto, config)
            guardarBaseDatos(baseDatos)
            messagebox.showinfo("Exito",
                f"Vehiculo estacionado en espacio {num}.\nVoucher generado en carpeta vouchers.")
            ventana.destroy()
            ventanaPadre.destroy()
    tk.Button(ventana, text="Estacionar", width=10,
          command=confirmar).grid(row=7, column=0, pady=10)
    tk.Button(ventana, text="Regresar",
            command=ventana.destroy).grid(row=7, column=1, pady=10)