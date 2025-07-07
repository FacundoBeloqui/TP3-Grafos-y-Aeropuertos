#!/usr/bin/python3

from datos import guardar_aeropuertos, guardar_vuelos, crear_dicc_ciudades
from programa import procesar_comando
from grafo import Grafo
import sys

def crear_grafo(vuelos):
    grafo = Grafo(es_dirigido=False)
    vertices = set(vuelos.keys())
    for origen in vuelos:
        for destino in vuelos[origen]:
            vertices.add(destino)
    for vertice in vertices:
        grafo.agregar_vertice(vertice)
    for origen in vuelos:
        for destino in vuelos[origen]:
            vuelo = vuelos[origen][destino]
            grafo.agregar_arista(origen, destino, vuelo)
    return grafo


def main():
    if len(sys.argv) != 3:
        sys.exit(1)

    archivo_aer = sys.argv[1]
    archivo_vue = sys.argv[2]

    aeropuertos = guardar_aeropuertos(archivo_aer)
    vuelos = guardar_vuelos(archivo_vue)
    dicc_ciudades = crear_dicc_ciudades(aeropuertos)
    grafo = crear_grafo(vuelos)
    ultima_salida = []
    centralidad_total = None

    for linea in sys.stdin:  
        linea = linea.strip()
        if not linea:
            continue
        ultima_salida = procesar_comando(linea, aeropuertos, vuelos, dicc_ciudades, grafo, ultima_salida, centralidad_total)


if __name__ == '__main__':
    main()
