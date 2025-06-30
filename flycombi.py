from grafo import Grafo

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

