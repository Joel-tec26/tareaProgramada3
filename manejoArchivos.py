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
    
# configuracion de tamaño

rutaConf = "configuracion.pkl"


def guardarConfiguracion(config):
    """
    Funcionalidad:
        Guarda el objeto Configuracion en memoria secundaria.
    Entrada:
        - config (Configuracion): Objeto con la configuracion del sistema.
    Salida:
        - (None)
    """
    archivo = open(rutaConf, "wb")
    pickle.dump(config, archivo)
    archivo.close()


def cargarConfiguracion():
    """
    Funcionalidad:
        Carga el objeto Configuracion desde memoria secundaria.
        Retorna None si el archivo no existe.
    Entrada:
        - (None)
    Salida:
        - config (Configuracion): Objeto con la configuracion del sistema.
    """
    try:
        archivo = open(rutaConf, "rb")
        config = pickle.load(archivo)
        archivo.close()
        return config
    except FileNotFoundError:
        return None


def existeConfiguracion():
    """
    Funcionalidad:
        Verifica si ya existe un archivo de configuracion en memoria secundaria.
    Entrada:
        - (None)
    Salida:
        - existe (bool): True si el archivo existe, False si no.
    """
    try:
        archivo = open(rutaConf, "rb")
        archivo.close()
        return True
    except FileNotFoundError:
        return False