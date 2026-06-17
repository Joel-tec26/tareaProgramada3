# Creado por: Joel Porras y Alexis Torres
# Fecha de creación: 15/06/2026 7:07am
# Ultima modificación: 15/06/2026 7:15am
# versión: 3.14

# importacion de librerias
import pickle

# definicion de funciones

baseDatos = "baseDatos.pkl"

def guardarBaseDatos(listaObjetos):
    """
    Funcionalidad:
        Serializa y guarda la lista de objetos Estacionamiento
        en memoria secundaria usando pickle.
    Entrada:
        - listaObjetos (list): Lista de objetos Estacionamiento.
    Salida:
        - (None)
    """
    archivo = open(baseDatos, "wb")
    pickle.dump(listaObjetos, archivo)
    archivo.close()


def cargarBaseDatos():
    """
    Funcionalidad:
        Carga la lista de objetos Estacionamiento desde memoria secundaria.
        Retorna lista vacía si el archivo no existe.
    Entrada:
        - (None)
    Salida:
        - listaObjetos (list): Lista de objetos Estacionamiento recuperada.
    """
    try:
        archivo = open(baseDatos, "rb")
        listaObjetos = pickle.load(archivo)
        archivo.close()
        return listaObjetos
    except FileNotFoundError:
        return []


def existeBaseDatos():
    """
    Funcionalidad:
        Verifica si ya existe un archivo de base de datos en memoria secundaria.
    Entrada:
        - (None)
    Salida:
        - existe (bool): True si el archivo existe, False si no.
    """
    try:
        archivo = open(baseDatos, "rb")
        archivo.close()
        return True
    except FileNotFoundError:
        return False