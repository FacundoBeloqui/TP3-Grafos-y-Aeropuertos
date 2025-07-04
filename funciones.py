from grafo import Grafo 
from biblioteca import camino_minimo_dijkstra, reconstruir_camino, bfs, mst_prim, calcular_centralidad, topologico_dfs


def obtener_aeropuertos(ciudades, origen, destino):

    aeropuertos_origen = ciudades[origen]
    aeropuertos_destino = set(ciudades[destino])

    if not aeropuertos_origen or not aeropuertos_destino:
        print("Origen o destino no encontrado")
        return None, None

    return aeropuertos_origen, aeropuertos_destino

def camino_minimo(grafo, ciudades, origen, destino, modo):
    origenes, destinos = obtener_aeropuertos(ciudades, origen, destino)
    if origenes is None:
        return

    mejor_camino = None
    mejor = float("inf")

    for aerop_origen in origenes:
        padre, dist = camino_minimo_dijkstra(grafo, modo, aerop_origen, destino)
        for aerop_destino in destinos:
            if aerop_destino in dist and dist[aerop_destino] < mejor:
                mejor_camino = reconstruir_camino(padre, aerop_destino)
                mejor = dist[aerop_destino]

    if mejor_camino:
        print(" -> ".join(mejor_camino))
    else:
        print("No se encontro camino")


def camino_mas_rapido(grafo_tiempo, ciudades, origen, destino):
    return camino_minimo(grafo_tiempo, ciudades, origen, destino, lambda vuelo: vuelo.tiempo)


def camino_mas_barato(grafo_precio, ciudades, origen, destino):
    return camino_minimo(grafo_precio, ciudades, origen, destino, lambda vuelo: vuelo.precio)


def camino_escalas(grafo_escalas, ciudades, origen, destino):
    aeropuertos_origen, aeropuertos_destino = obtener_aeropuertos(ciudades, origen, destino)

    mejor_camino = None
    menos_escalas = float("inf")

    for orig in aeropuertos_origen:
        padre, orden = bfs(grafo_escalas, orig)
        for dest in aeropuertos_destino:
            if dest in orden and orden[dest] < menos_escalas:
                mejor_camino = reconstruir_camino(padre, dest)
                menos_escalas = orden[dest]

    if mejor_camino:
        print(" -> ".join(mejor_camino))
    else:
        print("No se encontro camino")

def centralidad(grafo_precio, n):
    dicc_centralidad = calcular_centralidad(grafo_precio)
    dicc_ordenado = sorted(dicc_centralidad.items(), key=lambda x: (-x[1], x[0]))
    lista = []
    for aeropuerto, _ in dicc_ordenado[:n]:
        lista.append(aeropuerto)
    print(", ".join(lista))



def nueva_ruta(grafo, vuelos, archivo):
    arbol = mst_prim(grafo, lambda vuelo: vuelo.precio)  # devuelve Grafo no dirigido con solo las aristas del MST
    print(arbol.obtener_vertices())
    #with open(archivo, 'w') as f:
     #   for origen in arbol.obtener_vertices():
      #      for destino in arbol.adyacentes(origen):
       #         for vuelo in vuelos:
        #            if vuelo.origen == origen and vuelo.destino == destino:
         #               f.write(f"{vuelo.origen},{vuelo.destino},{vuelo.tiempo},{vuelo.precio},{vuelo.cant_vuelos}\n")
    print("OK")


def itinerario(grafo, dicc_ciudades, ruta):
    lineas = []
    with open(ruta) as f:
        for linea in f:
            lineas.append(linea.strip())
    
    ciudades = lineas[0].split(",")
    grafo_orden = Grafo(es_dirigido=True)
    
    for ciudad in ciudades:
        grafo_orden.agregar_vertice(ciudad)
    
    for i in range(1, len(lineas)):
        ciudad = lineas[i].split(",")
        grafo_orden.agregar_arista(ciudad[0].strip(), ciudad[1].strip()) 
    
    orden = topologico_dfs(grafo_orden)
    if len(orden) != len(ciudades):
        return

    print(", ".join(orden))
    for i in range(len(orden)-1):
        camino_escalas(grafo, dicc_ciudades, orden[i], orden[i+1])




    
