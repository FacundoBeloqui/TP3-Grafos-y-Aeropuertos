from datos import guardar_aeropuertos, guardar_vuelos, crear_dicc_ciudades
from funciones import camino_mas_rapido, camino_mas_barato, camino_escalas, centralidad, nueva_ruta, itinerario
from grafo import Grafo
import sys

def crear_grafo_frecuencia(vuelos):
    grafo = Grafo(es_dirigido=True)
    for origen in vuelos:
        for destino in vuelos[origen]:
            vuelo = vuelos[origen][destino]
            if vuelo.cant_vuelos > 0:
                peso = 1 / vuelo.cant_vuelos
            else:
                peso = float('inf')  # O un valor muy alto si no hay vuelos
            grafo.agregar_arista(origen, destino, peso)
    return grafo

'''---------mas rapido -----------'''
def crear_grafo_tiempo(vuelos):
    grafo = Grafo(es_dirigido=True)
    for origen in vuelos:
        for destino in vuelos[origen]:
            vuelo = vuelos[origen][destino]
            grafo.agregar_arista(origen, destino, vuelo.tiempo)
    return grafo


'''---------mas barato -----------'''

def crear_grafo_precio(vuelos):
    grafo = Grafo(es_dirigido=True)
    for origen in vuelos:
        for destino in vuelos[origen]:
            vuelo = vuelos[origen][destino]
            grafo.agregar_arista(origen, destino, vuelo.precio)
    return grafo

def crear_grafo_precio_no_dirigido(vuelos):
    grafo = Grafo(es_dirigido=False)
    for origen in vuelos:
        for destino in vuelos[origen]:
            vuelo = vuelos[origen][destino]
            grafo.agregar_arista(origen, destino, vuelo.precio)
    return grafo


'''---------menos escalas -----------'''

def crear_grafo_escalas(vuelos):
    grafo = Grafo(es_dirigido=True)
    for origen in vuelos:
        for destino in vuelos[origen]:
            grafo.agregar_arista(origen, destino, 1)
    return grafo

def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    archivo_aer = sys.argv[1]
    archivo_vue = sys.argv[2]
    aeropuertos = guardar_aeropuertos(archivo_aer)
    vuelos = guardar_vuelos(archivo_vue)
    dicc_ciudades = crear_dicc_ciudades(aeropuertos)

    grafo_tiempo = crear_grafo_tiempo(vuelos)
    grafo_precio = crear_grafo_precio(vuelos)
    grafo_precio_no_dirigido = crear_grafo_precio_no_dirigido(vuelos)
    grafo_escalas = crear_grafo_escalas(vuelos)
    grafo_frecuencias = crear_grafo_frecuencia(vuelos)

    for linea in sys.stdin:  #camino_mas rapido,San Diego,New York,  camino_escalas San Diego,New York
        linea = linea.strip()
        comando, params = linea.split(" ", 1)
        parametros = params.split(",")

        if not linea:
            continue

        match comando:
            case 'camino_mas':
                if len(parametros) != 3:
                    print("Error en cantidad de argumentos, deberian ser 3")
                else:
                    origen = parametros[1]
                    destino = parametros[2]
                    if parametros[0] == "rapido":
                        camino_mas_rapido(grafo_tiempo, dicc_ciudades, origen, destino)
                    elif parametros[0] == "barato":
                        camino_mas_barato(grafo_precio, dicc_ciudades, origen, destino)

            case 'camino_escalas':
                if len(parametros) != 2:
                    print("Error en cantidad de argumentos, deberian ser 2")
                else:
                    origen = parametros[0]
                    destino = parametros[1]
                    camino_escalas(grafo_escalas, dicc_ciudades, origen, destino)

            case 'centralidad':
                if len(parametros) != 1:
                    print("Error en cantidad de argumentos, deberian ser 1")
                else:
                    n = int(parametros[0])
                    centralidad(grafo_frecuencias, n)
                    
            case 'nueva_aerolinea':
                if len(parametros) != 1:
                    print("Error: se espera 1 parámetro (ruta del archivo)")
                else:
                    ruta_salida = parametros[0]
                    nueva_ruta(grafo_precio_no_dirigido, vuelos, ruta_salida)
            
            case 'itinerario':
                if len(parametros) != 1:
                    print("Error en cantidad de argumentos, deberian ser 1")
                else:
                    ruta = parametros[0]
                    itinerario(grafo_tiempo, dicc_ciudades, ruta)

            case 'salir':
                sys.exit(0)

            case _:
                print(f"Comando inválido o parámetros incorrectos: {linea}", file=sys.stderr)


if __name__ == '__main__':
    main()
