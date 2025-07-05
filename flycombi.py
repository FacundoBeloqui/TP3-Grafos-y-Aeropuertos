#!/usr/bin/python3

from datos import guardar_aeropuertos, guardar_vuelos, crear_dicc_ciudades
from funciones import camino_minimo, camino_escalas, centralidad, nueva_ruta, itinerario, exportar_kml
from grafo import Grafo
import sys

def crear_grafo(vuelos):
    grafo = Grafo(es_dirigido=False)
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

    for linea in sys.stdin:  #camino_mas rapido,San Diego,New York,  camino_escalas San Diego,New York
        linea = linea.strip()
        comando, params = linea.split(" ", 1)
        parametros = params.split(",")

        if not linea:
            continue

        if comando == 'camino_mas':
            if len(parametros) != 3:
                print("Error en cantidad de argumentos, deberian ser 3")
            else:
                origen = parametros[1]
                destino = parametros[2]
                if parametros[0] == "rapido":
                    ultima_salida = camino_minimo(grafo, dicc_ciudades, origen, destino, lambda vuelo: vuelo.tiempo)
                elif parametros[0] == "barato":
                    ultima_salida = camino_minimo(grafo, dicc_ciudades, origen, destino, lambda vuelo: vuelo.precio)

        elif comando ==  'camino_escalas':
            if len(parametros) != 2:
                print("Error en cantidad de argumentos, deberian ser 2")
            else:
                origen = parametros[0]
                destino = parametros[1]
                ultima_salida = camino_escalas(grafo, dicc_ciudades, origen, destino)

        elif comando == 'centralidad':
            if len(parametros) != 1:
                print("Error en cantidad de argumentos, deberian ser 1")
            else:
                n = int(parametros[0])
                centralidad(grafo, n)

        elif comando == 'nueva_aerolinea':
            if len(parametros) != 1:
                print("Error: se espera 1 parámetro (ruta del archivo)")
            else:
                ruta_salida = parametros[0]
                nueva_ruta(grafo, vuelos, ruta_salida)

        elif comando == 'itinerario':
            if len(parametros) != 1:
                print("Error en cantidad de argumentos, deberian ser 1")
            else:
                ruta = parametros[0]
                itinerario(grafo, dicc_ciudades, ruta)

        elif comando == "exportar_kml":
            if len(parametros) != 1:
                print("Error: se espera 1 parámetro (ruta del archivo)")
            else:
                ruta_archivo =parametros[0]
                exportar_kml(ultima_salida, aeropuertos, ruta_archivo)

        elif comando == 'salir':
            sys.exit(0)

        else:
            print(f"Comando inválido o parámetros incorrectos: {linea}", file=sys.stderr)


if __name__ == '__main__':
    main()
