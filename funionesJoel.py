# Creado por: Joel Porras y Alexis Torres
# Fecha de creación: 15/06/2026 7:16 am
# Ultima modificación: 15/06/2026 
# versión: 3.14

# importacion de librerias
import json
import random
from datetime import datetime, timedelta
from clase import Estacionamiento

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
        Toma los primeros registros según la cantidad indicada del JSON,
        extrae únicamente los campos requeridos y construye el diccionario
        con la estructura definida por la especificación.
    Entrada:
        - datosJson (list): Lista de registros crudos del archivo JSON.
        - cantidadVehiculos (int): Cantidad de vehículos a procesar.
        - montoPorHora (int): Monto parametrizado para el cobro por hora.
    Salida:
        - diccionario (dict): Diccionario {placa: [marca, color, tipo, ubicacion,
                              fechaHoraEntrada, fechaHoraSalida, monto, tipoPago]}.
    """
    diccionario = {}
    contador = 1

    for registro in datosJson[:cantidadVehiculos]:

        placa            = extraerPlaca(registro, contador)  # clave
        marca            = extraerMarca(registro)            # [0]
        color            = extraerColor(registro)            # [1]
        tipo             = extraerTipo(registro)             # [2]
        ubicacion        = str(contador)                     # [3]
        fechaHoraEntrada = generarFechaEntradaAleatoria()    # [4]
        fechaHoraSalida  = ""                                # [5]
        monto            = montoPorHora                      # [6] parametrizado
        tipoPago         = 0                                 # [7] 0=pendiente, 1=efectivo, 2=SINPE, 3=tarjeta

        diccionario[placa] = [marca, color,tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago ]
        contador += 1
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
