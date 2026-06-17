# Creado por: Joel Porras y Alexis Torres
# Fecha de creación: 16/06/2026 17:32 am
# Ultima modificación:
# versión: 3.14

# definición de clase

class Estacionamiento:
    """
    Funcionalidad:
        Representa un espacio de estacionamiento con la información del vehículo,
        su estadía y los datos de pago.
    Entrada:
        - identificador (str): Identificador del espacio.
        - info (tuple): (placa, marca, color, tipo) del vehículo.
        - estadia (list): [ubicacion, fechaHoraEntrada, fechaHoraSalida].
        - pago (tuple): (monto, tipoPago).
    Salida:
        - Objeto Estacionamiento instanciado.
    """
    def __init__(self, identificador, info, estadia, pago):
        self.id = identificador
        self.info = info
        self.estadia = estadia
        self.pago = pago

    def obtenerId(self):
        """
        Funcionalidad:
            Retorna el identificador del espacio.
        Entrada:
            - (None)
        Salida:
            - id (str): Identificador del espacio.
        """
        return self.id

    def obtenerInfo(self):
        """
        Funcionalidad:
            Retorna la tupla con la información del vehículo.
        Entrada:
            - (None)
        Salida:
            - info (tuple): (placa, marca, color, tipo).
        """
        return self.info

    def obtenerEstadia(self):
        """
        Funcionalidad:
            Retorna la lista con los datos de estadía del vehículo.
        Entrada:
            - (None)
        Salida:
            - estadia (list): [ubicacion, fechaHoraEntrada, fechaHoraSalida].
        """
        return self.estadia

    def obtenerPago(self):
        """
        Funcionalidad:
            Retorna la tupla con los datos de pago.
        Entrada:
            - (None)
        Salida:
            - pago (tuple): (monto, tipoPago).
        """
        return self.pago

    def asignarId(self, nuevoId):
        """
        Funcionalidad:
            Asigna el identificador del espacio.
        Entrada:
            - nuevoId (str): Nuevo identificador del espacio.
        Salida:
            - (None)
        """
        self.id = nuevoId

    def asignarInfo(self, nuevaInfo):
        """
        Funcionalidad:
            Asigna la tupla de información del vehículo.
        Entrada:
            - nuevaInfo (tuple): Nueva tupla (placa, marca, color, tipo).
        Salida:
            - (None)
        """
        self.info = nuevaInfo

    def asignarEstadia(self, nuevaEstadia):
        """
        Funcionalidad:
            Asigna la lista de estadía del vehículo.
        Entrada:
            - nuevaEstadia (list): Nueva lista [ubicacion, fechaHoraEntrada, fechaHoraSalida].
        Salida:
            - (None)
        """
        self.estadia = nuevaEstadia

    def asignarPago(self, nuevoPago):
        """
        Funcionalidad:
            Asigna la tupla de pago del vehículo.
        Entrada:
            - nuevoPago (tuple): Nueva tupla (monto, tipoPago).
        Salida:
            - (None)
        """
        self.pago = nuevoPago

    def mostrarTodo(self):
        """
        Funcionalidad:
            Imprime en consola todos los atributos del objeto
            de forma legible para el usuario.
        Entrada:
            - (None)
        Salida:
            - (None)
        """
        print(f"  ID             : {self.id}")
        print(f"  Placa          : {self.info[0]}")
        print(f"  Marca          : {self.info[1]}")
        print(f"  Color          : {self.info[2]}")
        print(f"  Tipo           : {self.info[3]}")
        print(f"  Ubicacion      : {self.estadia[0]}")
        print(f"  Hora entrada   : {self.estadia[1]}")
        print(f"  Hora salida    : {self.estadia[2]}")
        print(f"  Monto          : {self.pago[0]}")
        print(f"  Tipo de pago   : {self.pago[1]}")