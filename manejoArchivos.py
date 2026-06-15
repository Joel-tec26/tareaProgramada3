# Creado por: Joel Porras y Alexis Torres
# Fecha de creación: 15/06/2026 7:07am
# Ultima modificación: 15/06/2026 7:15am
# versión: 3.14

# importacion de librerias
import pickle

# definicion de funciones
archivoDonadores = "donadores.dat"

def cargarDatosDesdeArchivo():
    """
   función:Carga la lista almacenada en el archivo binario.
    Entradas:
        No recibe parámetros.
    Salidas:
        list: Lista de donadores cargada desde el archivo.
              Retorna una lista vacía si el archivo no existe
              o si ocurre un error de lectura.
    """
    try:
        with open(archivoDonadores, "rb") as archivo:
            return pickle.load(archivo)
    except FileNotFoundError:
        return []
    except (pickle.PickleError, EOFError):
        return []

def guardarEnArchivo(matrizGuardar):
    """
    funcion: Guarda en un archivo binario.
    entradas:
    - matrizGuardar: matriz con la información de los donadores.
    salidas:
    - Ninguna.
    """
    with open(archivoDonadores, "wb") as archivo:
        pickle.dump(matrizGuardar, archivo)
    return