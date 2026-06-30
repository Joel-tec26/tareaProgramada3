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
from tkinter import *
from tkinter import ttk, messagebox
from manejoArchivos import *
from fpdf import FPDF


"""
uso os para interactuar con el sistema de archivos en especifico
os.path.exists que verifica si la carpeta vouchers existe, os.makedirs que crea la carpeta vouchers si no existe, os.path.join que une rutas de 
forma compatible con cualquier sistema operativo. Pickle no puede realizar estas operaciones ya que solo sirve para serializar y guardar objetos Python en memoria secundaria
"""


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
    listaObjetos = config.obtenerListaObjetos()
    topeMaximoMasivo = calcularEspaciosDisponibles(config)
    ocupados = calcularEspaciosOcupados(listaObjetos)
    espaciosALlenar = topeMaximoMasivo - ocupados
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
        placa = placas[indiceVehiculo]
        datosVehiculo = diccionario[placa]
        posicion = ubicacionesLibres[indiceUbicacion]
        objeto  = listaObjetos[posicion]
        objeto.asignarInfo((placa, datosVehiculo[0], datosVehiculo[1], datosVehiculo[2]))
        objeto.asignarEstadia([str(posicion + 1), datosVehiculo[4], datosVehiculo[5]])
        objeto.asignarPago((datosVehiculo[6], datosVehiculo[7]))
        indiceVehiculo += 1
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
    imagenQR = qrcode.make(contenidoQR)
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
    tipo = tiposValidos[tipoIndice]

    fechaFormato = fechaHoraEntrada.replace("/", "-").replace(" ", "_").replace(":", "")
    nombrePdf = f"voucher_{placa}_{fechaFormato}.pdf"
    nombreQR = f"qr_{placa}_{fechaFormato}.png"
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
    

#  cierre diario 

def calcularMonto(fechaHoraEntrada, fechaHoraSalida, montoPorHora, tiempoGracia):
    """
    Funcionalidad:
        Calcula el monto a cobrar segun el tiempo de estadía,
        respetando el tiempo de gracia configurado.
    Entrada:
        - fechaHoraEntrada (str): Fecha y hora de entrada en formato DD/MM/AAAA HH:MM.
        - fechaHoraSalida (str): Fecha y hora de salida en formato DD/MM/AAAA HH:MM.
        - montoPorHora (int): Monto cobrado por hora en colones.
        - tiempoGracia (int): Minutos de gracia antes de cobrar.
    Salida:
        - monto (int): Monto total a cobrar en colones.
    """
    entrada = datetime.strptime(fechaHoraEntrada, "%d/%m/%Y %H:%M")
    salida  = datetime.strptime(fechaHoraSalida,  "%d/%m/%Y %H:%M")

    diferencia = salida - entrada
    minutosTotal = int(diferencia.total_seconds() / 60)
    if minutosTotal <= tiempoGracia:
        return 0
    horasCobrar = minutosTotal / 60
    monto       = int(horasCobrar * montoPorHora)
    return monto


def asignarTipoPagoAleatorio():
    """
    Funcionalidad:
        Asigna un tipo de pago aleatorio entre efectivo, SINPE y tarjeta.
    Entrada:
        - (None)
    Salida:
        - tipoPago (int): 1=efectivo, 2=SINPE, 3=tarjeta.
    """
    return random.randint(1, 3)


def convertirTipoPago(tipoPago):
    """
    Funcionalidad:
        Convierte el codigo de tipo de pago a texto legible.
    Entrada:
        - tipoPago (int): 1=efectivo, 2=SINPE, 3=tarjeta.
    Salida:
        - texto (str): Nombre del tipo de pago.
    """
    if tipoPago == 1:
        return "Efectivo"
    if tipoPago == 2:
        return "SINPE"
    return "Tarjeta"


def procesarPendientes(listaObjetos, config):
    """
    Funcionalidad:
        Recorre la lista de objetos y procesa todos los espacios ocupados
        sin pago registrado. Asigna hora de salida, tipo de pago aleatorio
        y calcula el monto. Genera la factura de cada uno.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - listaObjetos (list): Lista de objetos actualizada con pagos procesados.
    """
    horaSalida = datetime.now().strftime("%d/%m/%Y %H:%M")

    for objeto in listaObjetos:
        placa    = objeto.obtenerInfo()[0]
        tipoPago = objeto.obtenerPago()[1]

        if placa != "" and tipoPago == 0:
            monto    = calcularMonto(
                objeto.obtenerEstadia()[1],
                horaSalida,
                config.obtenerMontoPorHora(),
                config.obtenerTiempoGracia()
            )
            tipoPagoAleatorio = asignarTipoPagoAleatorio()

            objeto.asignarEstadia([
                objeto.obtenerEstadia()[0],
                objeto.obtenerEstadia()[1],
                horaSalida
            ])
            objeto.asignarPago((monto, tipoPagoAleatorio))
            generarFactura(objeto, config)

    return listaObjetos

def generarFactura(objeto, config):
    """
    Funcionalidad:
        Genera una factura en PDF con la informacion completa de la estadia
        del vehiculo y un codigo QR con los datos principales.
    Entrada:
        - objeto (Estacionamiento): Objeto con la informacion del vehiculo.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    placa  = objeto.obtenerInfo()[0]
    marcaIndice = objeto.obtenerInfo()[1]
    colorIndice = objeto.obtenerInfo()[2]
    tipoIndice = objeto.obtenerInfo()[3]
    ubicacion  = objeto.obtenerEstadia()[0]
    fechaHoraEntrada = objeto.obtenerEstadia()[1]
    fechaHoraSalida = objeto.obtenerEstadia()[2]
    monto = objeto.obtenerPago()[0]
    tipoPago = objeto.obtenerPago()[1]
    marca = marcasValidas[marcaIndice]
    color = coloresValidos[colorIndice]
    tipo = tiposValidos[tipoIndice]
    fechaFormato = fechaHoraSalida.replace("/", "-").replace(" ", "_").replace(":", "")
    nombrePdf = f"factura_{placa}_{fechaFormato}.pdf"
    nombreQR  = f"qr_factura_{placa}_{fechaFormato}.png"
    if not os.path.exists("facturas"):
        os.makedirs("facturas")
    rutaPdf = os.path.join("facturas", nombrePdf)
    rutaQR  = os.path.join("facturas", nombreQR)
    generarCodigoQR(placa, marca, tipo, fechaHoraEntrada, rutaQR)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_text_color(0, 51, 153)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 15, "Factura de Estacionamiento", ln=True, align="C")
    pdf.ln(3)
    pdf.set_text_color(80, 80, 80)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 10, "Informacion del vehiculo", ln=True)
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Placa          : {placa}",                    ln=True)
    pdf.cell(0, 8, f"Marca          : {marca}",                    ln=True)
    pdf.cell(0, 8, f"Color          : {color}",                    ln=True)
    pdf.cell(0, 8, f"Tipo           : {tipo}",                     ln=True)
    pdf.cell(0, 8, f"Ubicacion      : {ubicacion}",                ln=True)
    pdf.cell(0, 8, f"Hora entrada   : {fechaHoraEntrada}",         ln=True)
    pdf.cell(0, 8, f"Hora salida    : {fechaHoraSalida}",          ln=True)
    pdf.cell(0, 8, f"Tipo de pago   : {convertirTipoPago(tipoPago)}", ln=True)
    pdf.ln(3)
    pdf.set_text_color(0, 130, 0)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Total a pagar  : {monto} colones", ln=True)
    pdf.image(rutaQR, x=140, y=40, w=60, h=60)
    pdf.output(rutaPdf)



def generarReporteCierreDiario(listaObjetos, config):
    """
    Funcionalidad:
        Genera el reporte del cierre diario en PDF con titulo, fecha,
        tabla de transacciones, subtotales por tipo de pago y total acumulado.
        Usa 3 colores y 3 tamannos de letra segun la especificacion.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    fechaHoy = datetime.now().strftime("%d/%m/%Y")
    nombrePdf = f"cierre_diario_{fechaHoy.replace('/', '-')}.pdf"
    if not os.path.exists("reportes"):
        os.makedirs("reportes")
    rutaPdf = os.path.join("reportes", nombrePdf)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_text_color(0, 51, 153)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 15, "Reporte de Cierre Diario", ln=True, align="C")
    pdf.set_text_color(80, 80, 80)
    pdf.set_font("Helvetica", "I", 13)
    pdf.cell(0, 8, f"Fecha: {fechaHoy}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_text_color(0, 51, 153)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_fill_color(220, 230, 255)
    pdf.cell(20,  8, "Ubicac.", border=1, fill=True)
    pdf.cell(30,  8, "Placa", border=1, fill=True)
    pdf.cell(38,  8, "Entrada", border=1, fill=True)
    pdf.cell(38,  8, "Salida", border=1, fill=True)
    pdf.cell(28,  8, "Pago", border=1, fill=True)
    pdf.cell(28,  8, "Monto", border=1, fill=True, ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 9)
    montoEfectivo = 0
    montoSinpe    = 0
    montoTarjeta  = 0
    montoTotal    = 0
    for objeto in listaObjetos:
        placa    = objeto.obtenerInfo()[0]
        tipoPago = objeto.obtenerPago()[1]
        if placa != "" and tipoPago != 0:
            ubicacion        = objeto.obtenerEstadia()[0]
            fechaHoraEntrada = objeto.obtenerEstadia()[1]
            fechaHoraSalida  = objeto.obtenerEstadia()[2]
            monto            = objeto.obtenerPago()[0]
            pdf.cell(20,  7, str(ubicacion),  border=1)
            pdf.cell(30,  7, str(placa), border=1)
            pdf.cell(38,  7, str(fechaHoraEntrada), border=1)
            pdf.cell(38,  7, str(fechaHoraSalida), border=1)
            pdf.cell(28,  7, convertirTipoPago(tipoPago), border=1)
            pdf.cell(28,  7, f"{monto} col", border=1, ln=True)
            if tipoPago == 1:
                montoEfectivo += monto
            elif tipoPago == 2:
                montoSinpe += monto
            else:
                montoTarjeta  += monto
            montoTotal += monto
    pdf.ln(8)
    pdf.set_text_color(0, 130, 0)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, f"Efectivo  : {montoEfectivo} colones",  ln=True)
    pdf.cell(0, 8, f"SINPE     : {montoSinpe} colones",     ln=True)
    pdf.cell(0, 8, f"Tarjeta   : {montoTarjeta} colones",   ln=True)
    pdf.ln(3)
    pdf.set_text_color(0, 51, 153)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"Total acumulado del dia: {montoTotal} colones", ln=True)
    pdf.output(rutaPdf)
    print(f"Reporte guardado en: {rutaPdf}")

# esportar csv

def exportarCierreDiarioCSV(listaObjetos):
    """
    Funcionalidad:
        Exporta la tabla del cierre diario a un archivo CSV sin titulos,
        con los campos: ubicacion, placa, hora de entrada, hora de salida,
        tipo de pago y monto. Para abrirlo en Excel y corroborar la informacion.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
    Salida:
        - (None)
    """
    fechaHoy  = datetime.now().strftime("%d-%m-%Y")
    nombreCsv = f"cierre_diario_{fechaHoy}.csv"
    if not os.path.exists("reportes"):
        os.makedirs("reportes")
    rutaCsv = os.path.join("reportes", nombreCsv)
    archivo = open(rutaCsv, "w", encoding="utf-8-sig")
    # ya que excel lo coloca todo en una misma celda le estoy ingresando el separador que indica propiamente a Excel que el separador es punto y coma
    archivo.write("sep=;\n")

    for objeto in listaObjetos:
        placa  = objeto.obtenerInfo()[0]
        tipoPago = objeto.obtenerPago()[1]

        if placa != "" and tipoPago != 0:
            ubicacion = objeto.obtenerEstadia()[0]
            fechaHoraEntrada = objeto.obtenerEstadia()[1]
            fechaHoraSalida  = objeto.obtenerEstadia()[2]
            monto = objeto.obtenerPago()[0]
            linea = f"{ubicacion};{placa};{fechaHoraEntrada};{fechaHoraSalida};{convertirTipoPago(tipoPago)};{monto}\n"
            archivo.write(linea)
    archivo.close()
    print(f"CSV exportado en: {rutaCsv}")

#funciones alexis

def observarEspacio(baseDatos, config, num, valor):
    """
    Funcionalidad:
        Abre la ventana para observar un espacio del estacionamiento.
        Si esta ocupado muestra la informacion del vehiculo y permite pagar.
        Si esta libre permite estacionar un vehiculo.
    Entrada:
        - baseDatos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
        - num (int): Numero del espacio seleccionado.
        - valor (bool): True si el espacio esta ocupado, False si esta libre.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title(f"Estacionamiento: {num}")
    ventana.geometry("400x300")
    if not valor:
        tk.Label(ventana, text=f"Campo: {num}", font=("Arial", 20, "bold")).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(ventana, text="Este espacio se encuentra libre.", font=("Arial", 10)).grid(row=1, column=1, columnspan=2, padx=10, pady=20)
        tk.Button(ventana, text="Estacionar", width=10, height=3, bg="#B3F0FF", bd=0,
                  command=lambda: [ventana.destroy(), estacionarVehiculo(baseDatos, config, num, ventana)],
                  activebackground="#B3DDFF", cursor="hand2").grid(row=2, column=1, padx=10, pady=5)
    else:
        objeto = baseDatos[num - 1]
        tk.Label(ventana, text=f"Campo: {num}", font=("Arial", 20, "bold")).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(ventana, text="Placa: ", font=("Arial", 10)).grid(row=1, column=1, padx=10, pady=5)
        tk.Label(ventana, text=f"{objeto.obtenerInfo()[0]}", font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Marca: ", font=("Arial", 10)).grid(row=2, column=1, padx=10, pady=5)
        tk.Label(ventana, text=f"{marcasValidas[objeto.obtenerInfo()[1]]}", font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Color: ", font=("Arial", 10)).grid(row=3, column=1, padx=10, pady=5)
        tk.Label(ventana, text=f"{coloresValidos[objeto.obtenerInfo()[2]]}", font=("Arial", 10)).grid(row=3, column=2, padx=5, pady=2)
        tk.Label(ventana, text="Hora Entrada: ", font=("Arial", 10)).grid(row=4, column=1, padx=10, pady=5)
        tk.Label(ventana, text=f"{objeto.obtenerEstadia()[1]}", font=("Arial", 10)).grid(row=4, column=2, padx=5, pady=2)
        # solo se puede pagar si todavia no tiene tipo de pago asignado
        if objeto.obtenerPago()[1] == 0:
            tk.Button(ventana, text="Pagar", width=10, height=3, bg="#B3F0FF", bd=0,
                      command=lambda: abrirOpcionesPago(baseDatos, config, num, ventana),
                      activebackground="#B3DDFF", cursor="hand2").grid(row=5, column=1, padx=10, pady=5)
        else:
            tk.Label(ventana, text="Este vehiculo ya fue pagado.", font=("Arial", 10, "italic"), fg="green").grid(row=5, column=1, columnspan=2, padx=10, pady=5)
    tk.Button(ventana, text="Regresar", width=10, height=3, bg="#B3F0FF", bd=0,
              command=lambda: ventana.destroy(),
              activebackground="#B3DDFF", cursor="hand2").grid(row=6, column=2, padx=10, pady=5)


def abrirOpcionesPago(baseDatos, config, num, ventanaPadre):
    """
    Funcionalidad:
        Abre la ventana de seleccion del tipo de pago para un vehiculo
        ocupando un espacio, calcula el monto y registra el pago.
    Entrada:
        - baseDatos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
        - num (int): Numero del espacio a pagar.
        - ventanaPadre (Toplevel): Ventana de observarEspacio para cerrarla al pagar.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Seleccion de tipo de pago")
    ventana.geometry("400x150")
    tk.Label(ventana, text="Tipo de Pago", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    tk.Label(ventana, text="Seleccione el tipo de pago: ").grid(row=1, column=0, padx=10, pady=5)
    comboTipoPago = ttk.Combobox(ventana, values=["Efectivo", "SINPE", "Tarjeta"], state="readonly")
    comboTipoPago.grid(row=1, column=1, padx=10)
    comboTipoPago.current(0)

    def pagar():
        """
        Funcionalidad:
            Registra la hora de salida y el tipo de pago elegido,
            calcula el monto, genera el voucher/factura y guarda la BD.
        Entrada:
            - (None)
        Salida:
            - (None)
        """
        seleccion = comboTipoPago.get()
        if seleccion == "Efectivo":
            opcion = 1
        elif seleccion == "SINPE":
            opcion = 2
        else:
            opcion = 3

        objeto = baseDatos[num - 1]
        horaSalida = datetime.now().strftime("%d/%m/%Y %H:%M")
        monto = calcularMonto(
            objeto.obtenerEstadia()[1],
            horaSalida,
            config.obtenerMontoPorHora(),
            config.obtenerTiempoGracia()
        )
        objeto.asignarEstadia([objeto.obtenerEstadia()[0], objeto.obtenerEstadia()[1], horaSalida])
        objeto.asignarPago((monto, opcion))
        generarFactura(objeto, config)
        guardarBaseDatos(baseDatos)
        ventana.destroy()
        ventanaPadre.destroy()
        messagebox.showinfo("Exito", f"Pago realizado con exito.\nMonto: {monto} colones.\nFactura generada en carpeta 'facturas'.")

    tk.Button(ventana, text="Pagar", width=10, height=2, bg="#B3F0FF", bd=0,
              command=pagar, activebackground="#B3DDFF", cursor="hand2").grid(row=2, column=0, padx=10, pady=10)
    tk.Button(ventana, text="Cancelar", width=10, height=2, bg="#B3F0FF", bd=0,
              command=ventana.destroy, activebackground="#B3DDFF", cursor="hand2").grid(row=2, column=1, padx=10, pady=10)


def verEstacionamiento(tamanno, baseDatos, config):
    """
    Funcionalidad:
        Abre la ventana principal del estacionamiento con los espacios
        representados graficamente en verde (libre) o rojo (ocupado).
    Entrada:
        - tamanno (int): Tamanno total del estacionamiento.
        - baseDatos (list): Lista de objetos Estacionamiento.
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Estacionamiento")
    ventana.geometry("1020x720")
    tk.Label(ventana, text="Ver Estacionamiento", font=("Arial", 20, "bold")).grid(row=0, column=1, padx=10, pady=5)
    marcoEstacionamientos = tk.Frame(ventana)
    marcoEstacionamientos.grid(row=1, column=0, columnspan=3, sticky="w")

    def cambiarPagina(baseDatos, modo, pagina):
        """
        Funcionalidad:
            Cambia de pagina en la vista del estacionamiento.
            Modo 0 avanza a la siguiente pagina, modo 1 regresa a la anterior.
        Entrada:
            - baseDatos (list): Lista de objetos Estacionamiento.
            - modo (int): 0 para siguiente pagina, 1 para pagina anterior.
            - pagina (int): Pagina actual.
        Salida:
            - pagina (int): Nueva pagina.
        """
        if modo == 0:
            generarUI(baseDatos, pagina + 1)
            return pagina + 1
        elif modo == 1:
            generarUI(baseDatos, pagina - 1)
            return pagina - 1
        print("Error al tratar de llamar esta funcion, uso de modo incorrecto")

    def generarUI(baseDatos, pagina=0):
        """
        Funcionalidad:
            Genera la interfaz grafica de los espacios del estacionamiento
            para la pagina indicada.
        Entrada:
            - baseDatos (list): Lista de objetos Estacionamiento.
            - pagina (int): Pagina a mostrar.
        Salida:
            - (None)
        """
        for widget in marcoEstacionamientos.winfo_children():
            widget.destroy()
        for i in range(2):
            indice = 0
            for o in range(1, 9):
                indice = o + i * 8 + pagina * 16
                bandera = False
                if indice == tamanno:
                    break
                for carro in baseDatos:
                    if int(carro.obtenerEstadia()[0]) == indice and carro.obtenerInfo()[0] != "":
                        bandera = True
                borde = tk.Frame(marcoEstacionamientos,
                                 bg="#FF6E6E" if bandera else "#79FF96", padx=5, pady=5)
                borde.grid(row=i, column=o, padx=10, pady=80)
                # se usa lambda porque es la unica forma de pasar parametros en command,
                # sin este, el comando se ejecuta solo y usar el boton no serviria.
                # ademas, asigno variables en el lambda para que cada boton tenga
                # parametros unicos y no el mismo por ser generados en un for
                tk.Button(borde, text=f"{indice}", font=("Arial", 30, "bold"),
                          width=3, height=3,
                          bg="#FF5959" if bandera else "#59FF7D",
                          fg="#ffffff", bd=0,
                          command=lambda indice=indice, bandera=bandera: observarEspacio(baseDatos, config, indice, valor=bandera),
                          activebackground="#FF3F4F" if bandera else "#2EFF74",
                          cursor="hand2").grid()
            if indice + 1 >= tamanno:
                if 16 >= tamanno:
                    if 8 >= tamanno and i == 0:
                        break
                    if i == 1:
                        break
                borde = tk.Frame(marcoEstacionamientos, bg="#E5FFFE", padx=5, pady=5)
                borde.grid(row=0, column=9, padx=80, pady=80, sticky="e")
                tk.Button(borde, text="Anterior", width=8, height=5, bg="#B6FFFB", bd=0,
                          command=lambda pagina=pagina: cambiarPagina(baseDatos, modo=1, pagina=pagina),
                          activebackground="#B3F0FF", cursor="hand2").grid()
                break
            elif pagina == 0:
                if 16 >= tamanno:
                    if 8 >= tamanno and i == 0:
                        break
                    if i == 1:
                        break
                borde = tk.Frame(marcoEstacionamientos, bg="#E5FFFE", padx=5, pady=5)
                borde.grid(row=0, column=9, padx=80, pady=80, sticky="e")
                tk.Button(borde, text="Siguente", width=8, height=5, bg="#B6FFFB", bd=0,
                          command=lambda pagina=pagina: cambiarPagina(baseDatos, modo=0, pagina=pagina),
                          activebackground="#B3F0FF", cursor="hand2").grid()
            else:
                borde = tk.Frame(marcoEstacionamientos, bg="#E5FFFE", padx=5, pady=5)
                borde.grid(row=i, column=9, padx=80, pady=80)
                tk.Button(borde, text="Siguente" if i == 0 else "Anterior", width=8, height=5, bg="#B6FFFB", bd=0,
                          command=lambda i=i, pagina=pagina: cambiarPagina(baseDatos, modo=0, pagina=pagina) if i == 0 else cambiarPagina(baseDatos, modo=1, pagina=pagina),
                          activebackground="#B3F0FF", cursor="hand2").grid()

    generarUI(baseDatos)


def asignarInfoXml(baseDatos, tipo):
    """
    Funcionalidad:
        Construye el bloque XML con la informacion de todos los vehiculos
        que tienen el tipo de pago indicado.
    Entrada:
        - baseDatos (list): Lista de objetos Estacionamiento.
        - tipo (int): Tipo de pago a filtrar (1=efectivo, 2=SINPE, 3=tarjeta).
    Salida:
        - xml (str): Bloque XML con los carros de ese tipo de pago.
    """
    xml = ""
    for carro in baseDatos:
        if carro.obtenerPago()[1] == tipo:
            xml += "\t\t<carro>\n"
            xml += f"\t\t\t<placa>{carro.obtenerInfo()[0]}</placa>\n"
            xml += f"\t\t\t<marca>{marcasValidas[carro.obtenerInfo()[1]]}</marca>\n"
            xml += f"\t\t\t<color>{coloresValidos[carro.obtenerInfo()[2]]}</color>\n"
            xml += f"\t\t\t<tipo>{tiposValidos[carro.obtenerInfo()[3]]}</tipo>\n"
            xml += f"\t\t\t<ubicacion>{carro.obtenerEstadia()[0]}</ubicacion>\n"
            xml += f"\t\t\t<fechaHoraEntrada>{carro.obtenerEstadia()[1]}</fechaHoraEntrada>\n"
            xml += f"\t\t\t<fechaHoraSalida>{carro.obtenerEstadia()[2]}</fechaHoraSalida>\n"
            xml += f"\t\t\t<monto>{carro.obtenerPago()[0]}</monto>\n"
            xml += "\t\t</carro>\n"
    return xml


def generarReporteTipoPago(baseDatos):
    """
    Funcionalidad:
        Genera el reporte de cierre por tipo de pago en formato XML,
        agrupando los vehiculos pagados en efectivo, SINPE y tarjeta.
    Entrada:
        - baseDatos (list): Lista de objetos Estacionamiento.
    Salida:
        - (None)
    """
    efectivo = asignarInfoXml(baseDatos, 1)
    sinpe    = asignarInfoXml(baseDatos, 2)
    tarjeta  = asignarInfoXml(baseDatos, 3)

    xml  = "<reporte>\n"
    xml += "\t<efectivo>\n"
    xml += efectivo
    xml += "\t</efectivo>\n"
    xml += "\t<sinpe>\n"
    xml += sinpe
    xml += "\t</sinpe>\n"
    xml += "\t<tarjeta>\n"
    xml += tarjeta
    xml += "\t</tarjeta>\n"
    xml += "</reporte>"

    if not os.path.exists("reportes"):
        os.makedirs("reportes")
    rutaXml = os.path.join("reportes", "Reporte-Por-Tipo-De-Pago.xml")
    archivo = open(rutaXml, "w", encoding="utf-8")
    archivo.write(xml)
    archivo.close()
    messagebox.showinfo("Exito", f"Reporte por tipo de pago generado en:\n{rutaXml}")


def esNumero(valor):
    """
    Funcionalidad:
        Verifica si una cadena puede convertirse en un numero entero.
    Entrada:
        - valor (str): Cadena a validar.
    Salida:
        - esValido (bool): True si la cadena es un numero entero valido.
    """
    try:
        int(valor)
        return True
    except ValueError:
        return False


def tamannoEstacionamiento(config):
    """
    Funcionalidad:
        Abre la ventana para modificar el tamanno del estacionamiento
        y guarda el cambio en la configuracion.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Cambiar tamaño de estacionamiento")
    ventana.geometry("450x150")
    ventana.resizable(False, False)
    tk.Label(ventana, text="Cambiar tamaño de estacionamiento", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    tk.Label(ventana, text="Ingrese el nuevo tamaño: ").grid(row=1, column=0, padx=10, pady=5)
    entrada = tk.Entry(ventana, font=("Arial", 10))
    entrada.grid(row=1, column=1, padx=10, pady=2)

    def confirmar():
        """
        Funcionalidad:
            Valida el numero ingresado, confirma con el usuario y
            actualiza el tamanno en la configuracion.
        Entrada:
            - (None)
        Salida:
            - (None)
        """
        valor = entrada.get()
        if not esNumero(valor) or valor == "":
            messagebox.showerror("Error", "Solo puede ingresar datos numericos.")
            return
        confirmacion = messagebox.askyesno("Confirmar", f"Desea cambiar el tamaño a {valor}?")
        if confirmacion:
            config.asignarTamanno(int(valor))
            guardarConfiguracion(config)
            messagebox.showinfo("Exito", "Cambio realizado con exito.")
            ventana.destroy()

    tk.Button(ventana, text="Cambiar", command=confirmar).grid(row=2, column=0, pady=10)
    tk.Button(ventana, text="Atras", command=ventana.destroy).grid(row=2, column=1, pady=10)


def tiempoGraciaEnMinutos(config):
    """
    Funcionalidad:
        Abre la ventana para modificar el tiempo de gracia en minutos
        y guarda el cambio en la configuracion.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Cambiar tiempo de gracia")
    ventana.geometry("450x150")
    ventana.resizable(False, False)
    tk.Label(ventana, text="Cambiar tiempo de gracia en minutos", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    tk.Label(ventana, text="Ingrese el nuevo tiempo: ").grid(row=1, column=0, padx=10, pady=5)
    entrada = tk.Entry(ventana, font=("Arial", 10))
    entrada.grid(row=1, column=1, padx=10, pady=2)

    def confirmar():
        """
        Funcionalidad:
            Valida el numero ingresado, confirma con el usuario y
            actualiza el tiempo de gracia en la configuracion.
        Entrada:
            - (None)
        Salida:
            - (None)
        """
        valor = entrada.get()
        if not esNumero(valor) or valor == "":
            messagebox.showerror("Error", "Solo puede ingresar datos numericos.")
            return
        confirmacion = messagebox.askyesno("Confirmar", f"Desea cambiar el tiempo de gracia a {valor} minutos?")
        if confirmacion:
            config.asignarTiempoGracia(int(valor))
            guardarConfiguracion(config)
            messagebox.showinfo("Exito", "Cambio realizado con exito.")
            ventana.destroy()

    tk.Button(ventana, text="Cambiar", command=confirmar).grid(row=2, column=0, pady=10)
    tk.Button(ventana, text="Atras", command=ventana.destroy).grid(row=2, column=1, pady=10)


def montoPorHora(config):
    """
    Funcionalidad:
        Abre la ventana para modificar el monto cobrado por hora
        y guarda el cambio en la configuracion.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    ventana = tk.Toplevel()
    ventana.title("Modificar monto por hora")
    ventana.geometry("450x150")
    ventana.resizable(False, False)
    tk.Label(ventana, text="Modificar monto por hora", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=5)
    tk.Label(ventana, text="Ingrese el nuevo monto: ").grid(row=1, column=0, padx=10, pady=5)
    entrada = tk.Entry(ventana, font=("Arial", 10))
    entrada.grid(row=1, column=1, padx=10, pady=2)

    def confirmar():
        """
        Funcionalidad:
            Valida el numero ingresado, confirma con el usuario y
            actualiza el monto por hora en la configuracion.
        Entrada:
            - (None)
        Salida:
            - (None)
        """ 
        valor = entrada.get()
        if not esNumero(valor) or valor == "":
            messagebox.showerror("Error", "Solo puede ingresar datos numericos.")
            return
        confirmacion = messagebox.askyesno("Confirmar", f"Desea cambiar el monto por hora a {valor} colones?")
        if confirmacion:
            config.asignarMontoPorHora(int(valor))
            guardarConfiguracion(config)
            messagebox.showinfo("Exito", "Cambio realizado con exito.")
            ventana.destroy()
    tk.Button(ventana, text="Cambiar", command=confirmar).grid(row=2, column=0, pady=10)
    tk.Button(ventana, text="Atras", command=ventana.destroy).grid(row=2, column=1, pady=10)