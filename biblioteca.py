from grafo import Grafo
from collections import deque
import heapq

class UnionFind:
    def __init__(self, elems):
        #self.groups = {e: e for e in elems}
        self.groups = {}
        for e in elems:
            self.groups[e] = e

    def find(self, v):
        if self.groups[v] == v:
            return v

        real_group = self.find(self.groups[v])
        # plancho la estructura
        self.groups[v] = real_group
        return real_group

    def union(self, u, v):
        new_group = self.find(u)
        other = self.find(v)
        self.groups[other] = new_group

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

def camino_minimo_dijkstra(grafo, obtener_peso, origen, destino):
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
            vuelo = grafo.peso_arista(v, w)
            peso = obtener_peso(vuelo)
            nueva = dist[v] + peso
            if nueva < dist[w]:
                dist[w] = nueva
                padre[w] = v
                heapq.heappush(heap, (nueva, w))
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

def mst_prim(grafo, obtener_peso):
    v = grafo.vertice_aleatorio()
    visitados = set()
    visitados.add(v)
    heap = []
    for w in grafo.adyacentes(v):
        vuelo = grafo.peso_arista(v, w)
        peso = obtener_peso(vuelo)
        heapq.heappush(heap, (peso, v, w))
    arbol = Grafo(es_dirigido=False, vertices_init=grafo.obtener_vertices())
    while heap:
        peso, v, w = heapq.heappop(heap)
        if w in visitados:
            continue
        arbol.agregar_arista(v, w, peso)
        visitados.add(w)
        for x in grafo.adyacentes(w):
            if x not in visitados:
                vuelo_vecino = grafo.peso_arista(w, x)
                peso_vecino = obtener_peso(vuelo_vecino)
                heapq.heappush(heap, (peso_vecino, w, x))
    return arbol

def mst_kruskal(grafo):
    uf = UnionFind(grafo.obtener_vertices())
    aristas = obtener_aristas(grafo)
    aristas.sort(key=lambda tpl: tpl[2].precio)
    mst = Grafo(es_dirigido=False, vertices_init=grafo.obtener_vertices())
    for v, w, vuelo in aristas:
        if uf.find(v) != uf.find(w):
            mst.agregar_arista(v, w, vuelo.precio)
            uf.union(v, w)

    return mst


def calcular_centralidad(grafo):
    cent = {}
    for v in grafo.obtener_vertices(): cent[v] = 0
    for v in grafo.obtener_vertices():
        padre, distancia = camino_minimo_dijkstra(grafo, lambda vuelo: 1/vuelo.cant_vuelos if vuelo.cant_vuelos != 0 else float("inf"), v, None)
        cent_aux = {}
        for w in grafo.obtener_vertices():
            cent_aux[w] = 0
        vertices_ordenados = sorted(distancia, key=distancia.get, reverse=True)
        for w in vertices_ordenados:
            p = padre.get(w)
            if p is None or p not in cent_aux:
                continue
            cent_aux[p] += 1 + cent_aux[w]
        for w in grafo.obtener_vertices():
            if w == v: continue
            cent[w] += cent_aux[w]
    return cent


def _dfs(grafo, v, visitados, pila):
    visitados.add(v)
    for w in grafo.adyacentes(v):
        if w not in visitados:
            visitados.add(w)
            _dfs(grafo, w, visitados, pila)
    pila.append(v)


def topologico_dfs(grafo):
    visitados = set()
    pila = []
    for v in grafo.obtener_vertices():
        if v not in visitados:
            _dfs(grafo, v, visitados, pila)
    return pila[::-1]
