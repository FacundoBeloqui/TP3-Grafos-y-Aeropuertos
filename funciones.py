from grafo import Grafo 
from biblioteca import camino_minimo_dijkstra, reconstruir_camino, bfs, mst_kruskal, calcular_centralidad, topologico_dfs
import heapq


def obtener_aeropuertos(ciudades, origen, destino):

    aeropuertos_origen = ciudades.get(origen, [])
    aeropuertos_destino = ciudades.get(destino, [])

    if not aeropuertos_origen or not aeropuertos_destino:
        return None, None

    return aeropuertos_origen, aeropuertos_destino


def imprimir_camino(mejor_camino, char):
    print(char.join(mejor_camino))


def camino_minimo(grafo, ciudades, origen, destino, modo):
    origenes, destinos = obtener_aeropuertos(ciudades, origen, destino)
    if origenes is None:
        return []

    mejor_camino = None
    mejor = float("inf")

    for aerop_origen in origenes:
        padre, dist = camino_minimo_dijkstra(grafo, modo, aerop_origen, destino)
        for aerop_destino in destinos:
            if aerop_destino in dist and dist[aerop_destino] < mejor:
                mejor_camino = reconstruir_camino(padre, aerop_destino)
                mejor = dist[aerop_destino]

    if mejor_camino:
        imprimir_camino(mejor_camino, " -> ")
        return mejor_camino
    else:
        print("No se encontro camino")
        return []


def camino_escalas(grafo_escalas, ciudades, origen, destino):
    aeropuertos_origen, aeropuertos_destino = obtener_aeropuertos(ciudades, origen, destino)
    if aeropuertos_origen is None:
        return []

    mejor_camino = []

    for orig in aeropuertos_origen:
        padre, orden = bfs(grafo_escalas, orig)
        for dest in aeropuertos_destino:
            if dest in orden:
                camino = reconstruir_camino(padre, dest)
                if not mejor_camino or len(camino) < len(mejor_camino):
                    mejor_camino = camino


    if mejor_camino:
        imprimir_camino(mejor_camino, " -> ")
        return mejor_camino
    else:
        print("No se encontro camino")
        return []

def centralidad(grafo_precio, n, centralidad_total):
    if centralidad_total is None:
        dicc_centralidad = calcular_centralidad(grafo_precio, lambda vuelo: 1/vuelo.cant_vuelos if vuelo.cant_vuelos != 0 else float("inf"))
    top_n = heapq.nlargest(n, dicc_centralidad.items(), key=lambda x: x[1])
    lista = []
    for aeropuerto, _ in top_n:
        lista.append(aeropuerto)
    imprimir_camino(lista, ", ")


def nueva_ruta(grafo, vuelos, archivo):
    arbol_tendido_minimo = mst_kruskal(grafo, lambda vuelo: vuelo.precio)
    with open(archivo, 'w') as f:
        for origen in arbol_tendido_minimo.obtener_vertices():
            for destino in arbol_tendido_minimo.adyacentes(origen):
                if origen < destino:
                    if destino in vuelos.get(origen, {}):
                        vuelo = vuelos[origen][destino]
                    elif origen in vuelos.get(destino, {}):
                        vuelo = vuelos[destino][origen]
                    else:
                        continue
                    f.write(f"{origen},{destino},{vuelo.tiempo},{vuelo.precio},{vuelo.cant_vuelos}\n")
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
        par_ciudades = lineas[i].split(",")
        grafo_orden.agregar_arista(par_ciudades[0].strip(), par_ciudades[1].strip()) 
    
    orden = topologico_dfs(grafo_orden)
    if len(orden) != len(ciudades):
        return

    imprimir_camino(orden, ", ")
    for i in range(len(orden)-1):
        camino_escalas(grafo, dicc_ciudades, orden[i], orden[i+1])


def exportar_kml(ultima_salida, aeropuertos, ruta_archivo):
    if not ultima_salida or len(ultima_salida) < 2:
        print("No hay ruta para exportar")
        return

    with open(ruta_archivo, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<kml xmlns="http://earth.google.com/kml/2.1">\n')
        f.write('  <Document>\n')
        f.write('       <name>KML caminos minimos</name>\n')
        f.write('       <description>KML caminos minimos</description>\n')
        f.write('\n')
        for codigo in ultima_salida:
            aeropuerto = aeropuertos[codigo]
            f.write('    <Placemark>\n')
            f.write(f'       <name>{aeropuerto.codigo}</name>\n')
            f.write('        <Point>\n')
            f.write(f'          <coordinates>{aeropuerto.latitud}, {aeropuerto.longitud}</coordinates>\n')
            f.write('        </Point>\n')
            f.write('    </Placemark>\n')
            f.write('\n')

        for i in range(len(ultima_salida)-1):
            codigo_origen = ultima_salida[i]
            codigo_destino = ultima_salida[i+1]
            aeropuerto_o = aeropuertos[codigo_origen]
            aeropuerto_d = aeropuertos[codigo_destino]
            f.write('    <Placemark>\n')
            f.write('      <LineString>\n')
            f.write(f'        <coordinates>{aeropuerto_o.latitud}, {aeropuerto_o.longitud} {aeropuerto_d.latitud}, {aeropuerto_d.longitud}</coordinates>\n')
            f.write('      </LineString>\n')
            f.write('    </Placemark>\n')
            f.write('\n')

        f.write('  </Document>\n')
        f.write('</kml>')
    print("OK")

    
