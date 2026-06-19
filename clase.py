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


# clase de configurcion

class Configuracion:
    """
    Funcionalidad:
        Almacena la configuracion general del sistema de estacionamiento.
    Entrada:
        - tamano (int): Cantidad de espacios del estacionamiento.
        - montoPorHora (int): Monto cobrado por hora en colones.
        - tiempoGracia (int): Minutos de gracia antes de cobrar.
        - tieneElectrico (bool): Indica si el parqueo tiene espacio electrico.
        - listaObjetos (list): Lista de objetos Estacionamiento (base de datos).
    Salida:
        - Objeto Configuracion instanciado.
    """
    def __init__(self, tamanno, montoPorHora, tiempoGracia, tieneElectrico, listaObjetos):
        self.tamanno         = tamanno
        self.montoPorHora   = montoPorHora
        self.tiempoGracia   = tiempoGracia
        self.tieneElectrico = tieneElectrico
        self.listaObjetos   = listaObjetos

    def obtenerTamanno(self):
        """
        Funcionalidad:
            Retorna el tamanno del estacionamiento.
        Entrada:
            - (None)
        Salida:
            - tamano (int): Cantidad de espacios del estacionamiento.
        """
        return self.tamanno

    def obtenerMontoPorHora(self):
        """
        Funcionalidad:
            Retorna el monto cobrado por hora.
        Entrada:
            - (None)
        Salida:
            - montoPorHora (int): Monto en colones por hora.
        """
        return self.montoPorHora

    def obtenerTiempoGracia(self):
        """
        Funcionalidad:
            Retorna el tiempo de gracia en minutos.
        Entrada:
            - (None)
        Salida:
            - tiempoGracia (int): Minutos de gracia antes de cobrar.
        """
        return self.tiempoGracia

    def obtenerTieneElectrico(self):
        """
        Funcionalidad:
            Retorna si el parqueo tiene espacio para vehiculo electrico.
        Entrada:
            - (None)
        Salida:
            - tieneElectrico (bool): True si tiene espacio electrico.
        """
        return self.tieneElectrico

    def obtenerListaObjetos(self):
        """
        Funcionalidad:
            Retorna la lista de objetos Estacionamiento.
        Entrada:
            - (None)
        Salida:
            - listaObjetos (list): Lista de objetos Estacionamiento.
        """
        return self.listaObjetos

    def asignarTamanno(self, nuevoTamanno):
        """
        Funcionalidad:
            Asigna el tamanno del estacionamiento.
        Entrada:
            - nuevoTamano (int): Nueva cantidad de espacios.
        Salida:
            - (None)
        """
        self.tamanno = nuevoTamanno

    def asignarMontoPorHora(self, nuevoMonto):
        """
        Funcionalidad:
            Asigna el monto cobrado por hora.
        Entrada:
            - nuevoMonto (int): Nuevo monto en colones por hora.
        Salida:
            - (None)
        """
        self.montoPorHora = nuevoMonto

    def asignarTiempoGracia(self, nuevoTiempoGracia):
        """
        Funcionalidad:
            Asigna el tiempo de gracia en minutos.
        Entrada:
            - nuevoTiempoGracia (int): Nuevos minutos de gracia.
        Salida:
            - (None)
        """
        self.tiempoGracia = nuevoTiempoGracia

    def asignarTieneElectrico(self, nuevoTieneElectrico):
        """
        Funcionalidad:
            Asigna si el parqueo tiene espacio para vehiculo electrico.
        Entrada:
            - nuevoTieneElectrico (bool): True si tiene espacio electrico.
        Salida:
            - (None)
        """
        self.tieneElectrico = nuevoTieneElectrico

    def asignarListaObjetos(self, nuevaLista):
        """
        Funcionalidad:
            Asigna la lista de objetos Estacionamiento.
        Entrada:
            - nuevaLista (list): Nueva lista de objetos Estacionamiento.
        Salida:
            - (None)
        """
        self.listaObjetos = nuevaLista

    def mostrarTodo(self):
        """
        Funcionalidad:
            Imprime en consola todos los atributos de la configuracion
            de forma legible para el usuario.
        Entrada:
            - (None)
        Salida:
            - (None)
        """
        print(f"  Tamanno            : {self.tamanno}")
        print(f"  Monto por hora     : {self.montoPorHora}")
        print(f"  Tiempo de gracia   : {self.tiempoGracia} minutos")
        print(f"  Espacio electrico  : {'Si' if self.tieneElectrico else 'No'}")
        print(f"  Objetos en base de datos      : {len(self.listaObjetos)}")