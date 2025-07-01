from datos import guardar_aeropuertos, guardar_vuelos, crear_dicc_ciudades
from funciones import camino_mas_rapido, camino_mas_barato, camino_escalas, centralidad
from grafo import Grafo
import sys

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
    grafo_escalas = crear_grafo_escalas(vuelos)

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
                    centralidad()
            case 'salir':
                sys.exit(0)

            case _:
                print(f"Comando inválido o parámetros incorrectos: {linea}", file=sys.stderr)


if __name__ == '__main__':
    main()
