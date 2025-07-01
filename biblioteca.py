from grafo import Grafo
from collections import deque
import heapq

def bfs(grafo, origen):
    visitados = set()
    padres = {}
    orden = {}
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    q = deque()
    q.append(origen)
    while q:
        v = q.popleft()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                q.append(w)
    return padres, orden

def _dfs(grafo, v, visitados, padres, orden):
    for w in grafo.adyacentes(v):
        if w not in visitados:
            visitados.add(w)
            padres[w] = v
            orden[w] = orden[v] + 1
            _dfs(grafo, w, visitados, padres, orden)


def dfs(grafo, origen):
    padres = {}
    orden = {}
    visitados = set()
    padres[origen] = None
    orden[origen] = 0
    visitados.add(origen)
    _dfs(grafo, origen, visitados, padres, orden)
    return padres, orden

def recorrido_dfs_completo(grafo):
    visitados = set()
    padres = {}
    orden = {}
    for v in grafo.obtener_vertices():
        if v not in visitados:
            visitados.add(v)
            padres[v] = None
            orden[v] = 0
            _dfs(grafo, v, visitados, padres, orden)
    return padres, orden


def reconstruir_camino(padres, destino):
    recorrido = []
    while destino is not None:
        recorrido.append(destino)
        destino = padres[destino]
    return recorrido[::-1]

def camino_minimo_dijkstra(grafo, origen, destino):
    dist = {}
    padre = {}
    for v in grafo.obtener_vertices():
        dist[v] = float("inf")
    dist[origen] = 0
    padre[origen] = None
    heap = []
    heapq.heappush(heap, (dist[origen], origen))
    while heap:
        _, v = heapq.heappop(heap)
        if v == destino:
            return padre, dist
        for w in grafo.adyacentes(v):
            distancia_por_aca = dist[v] + grafo.peso_arista(v, w)
            if distancia_por_aca < dist[w]:
                dist[w] = distancia_por_aca
                padre[w] = v
                heapq.heappush(heap, (dist[w], w))
    return padre, dist


def obtener_aristas(grafo):
    aristas = []
    for v in grafo.obtener_vertices():
        for w in grafo.adyacentes(v):
            aristas.append((v, w, grafo.peso_arista(v, w)))
    return aristas


def camino_minimo_bf(grafo, origen):
    distancia = {}
    padre = {}
    for v in grafo.obtener_vertices():
        distancia[v] = float("inf")
    distancia[origen] = 0
    padre[origen] = None
    aristas = obtener_aristas(grafo)
    for i in range(len(grafo)):
        cambio = False
        for origen, destino, peso in aristas:
            if distancia[origen] + peso < distancia[destino]:
                cambio = True
                padre[destino] = origen
                distancia[destino] = distancia[origen] + peso
        if not cambio:
            return padre, distancia

    for v, w, peso in aristas:
        if distancia[v] + peso < distancia[w]:
            return None
    return padre, distancia

def mst_prim(grafo):
    v = grafo.vertice_aleatorio()
    visitados = set()
    visitados.add(v)
    heap = []
    for w in grafo.adyacentes(v):
        peso = grafo.peso_arista(v, w)
        heapq.heappush(heap, (v, w, peso))
    arbol = Grafo(es_dirigido=False, vertices_init=grafo.obtener_vertices())
    while heap:
        v, w, peso = heapq.heappop(heap)
        if w in visitados:
            continue
        arbol.agregar_arista(v, w, peso)
        visitados.add(w)
        for x in grafo.adyacentes(w):
            if x not in visitados:
                peso_vecino = grafo.peso_arista(w, x)
                heapq.heappush(heap, (w, x, peso_vecino))
    return arbol

