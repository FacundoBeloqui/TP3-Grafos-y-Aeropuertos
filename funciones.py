from biblioteca import camino_minimo_dijkstra, reconstruir_camino, bfs, mst_prim, calcular_centralidad


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

def centralidad(grafo_precio, n):
    dicc_centralidad = calcular_centralidad(grafo_precio)
    dicc_ordenado = sorted(dicc_centralidad.items(), key=lambda x: x[1], reverse=True)
    lista = []
    for aeropuerto, _ in dicc_ordenado[:n]:
        lista.append(aeropuerto)
    print(", ".join(lista))



def nueva_ruta(grafo_precio, vuelos, archivo):
    arbol = mst_prim(grafo_precio)  # devuelve Grafo no dirigido con solo las aristas del MST
    with open(archivo, 'w') as f:
        for origen in arbol.obtener_vertices():
            for destino in arbol.adyacentes(origen):
                # evitar duplicados: solo una dirección
                if origen < destino:
                    # buscar el vuelo real para obtener datos completos
                    if destino in vuelos.get(origen, {}):
                        vuelo = vuelos[origen][destino]
                    elif origen in vuelos.get(destino, {}):
                        vuelo = vuelos[destino][origen]
                        origen, destino = destino, origen
                    else:
                        continue
                    f.write(f"{origen},{destino},{vuelo.tiempo},{vuelo.precio},{vuelo.cant_vuelos}\n")
    print("OK")

