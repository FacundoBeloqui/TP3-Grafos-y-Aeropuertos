from dataclasses import dataclass

@dataclass
class Aeropuerto:
    ciudad: str
    codigo: str 
    latitud: float
    longitud: float

@dataclass
class Vuelo:
    origen: str
    destino: str
    tiempo: int
    precio: int
    cant_vuelos: int


def guardar_aeropuertos(archivo): #{codigo, Aeropuerto}
    aeropuertos = {}
    with open(archivo) as f:
        for linea in f:
            datos = linea.strip().split(",")
            ciudad = datos[0]
            codigo = datos[1]
            latitud = datos[2]
            longitud = datos[3]

            aeropuertos[codigo] = Aeropuerto(ciudad, codigo,float(latitud), float(longitud))
    
    return aeropuertos


def guardar_vuelos(archivo): #{origen, {destino, Vuelo}}
    vuelos = {}
    with open(archivo) as f:
        for linea in f:
            datos = linea.strip().split(",")
            origen = datos[0]
            destino = datos[1]
            tiempo = datos[2]
            precio = datos[3]
            cant_vuelos = datos[4]

            if origen not in vuelos:
                vuelos[origen] = {}
            vuelos[origen][destino] = Vuelo(origen, destino, int(tiempo), int(precio), int(cant_vuelos))

    return vuelos


def crear_dicc_ciudades(aeropuertos):
    ciudades = {}
    for aeropuerto in aeropuertos.values():
        if aeropuerto.ciudad not in ciudades:
            ciudades[aeropuerto.ciudad] = []
        ciudades[aeropuerto.ciudad].append(aeropuerto.codigo)
    return ciudades