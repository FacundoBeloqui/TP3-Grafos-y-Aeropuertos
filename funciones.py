from biblioteca import camino_minimo_dijkstra, reconstruir_camino, bfs

def obtener_aeropuertos(ciudades, origen, destino):
    aeropuertos_origen = ciudades.get(origen, [])
    aeropuertos_destino = ciudades.get(destino, [])
     
    if not aeropuertos_origen or not aeropuertos_destino:
        print("Origen o destino no encontrado")
        return None, None
    return aeropuertos_origen, aeropuertos_destino


def camino_minimo(grafo, ciudades, origen, destino):
    aeropuertos_origen, aeropuertos_destino = obtener_aeropuertos(ciudades, origen, destino)
    if aeropuertos_origen is None:
        return
    
    mejor_camino = None
    mejor = float("inf")

    for orig in aeropuertos_origen:
        padre, dist = camino_minimo_dijkstra(grafo, orig, None)
        for dest in aeropuertos_destino:
            if dest in dist and dist[dest] < mejor:
                mejor_camino = reconstruir_camino(padre, dest)
                mejor = dist[dest]
    
    if mejor_camino:
        print(" -> ".join(mejor_camino))
    else:
        print("No se encontro camino")


def camino_mas_rapido(grafo_tiempo, ciudades, origen, destino):
    return camino_minimo(grafo_tiempo, ciudades, origen, destino)


def camino_mas_barato(grafo_precio, ciudades, origen, destino):
    return camino_minimo(grafo_precio, ciudades, origen, destino)

 
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
