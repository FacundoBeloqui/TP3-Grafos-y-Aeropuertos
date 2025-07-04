import random

class Grafo:
    def __init__(self, es_dirigido=False, vertices_init=None):
        if vertices_init is None:
            vertices_init = []
        self.es_dirigido = es_dirigido
        self.adyacencia = {}
        for v in vertices_init:
            self.agregar_vertice(v)

    def agregar_vertice(self, v):
        if v not in self.adyacencia:
            self.adyacencia[v] = {}

    def borrar_vertice(self, v):
        if v not in self.adyacencia:
            return
        del self.adyacencia[v]
        for ady in self.adyacencia.values():
            if v in ady:
                del ady[v]

    def agregar_arista(self, v, w, peso=1):
        self.agregar_vertice(v)
        self.agregar_vertice(w)
        self.adyacencia[v][w] = peso
        if not self.es_dirigido:
            self.adyacencia[w][v] = peso

    def borrar_arista(self, v, w):
        if v in self.adyacencia and w in self.adyacencia[v]:
            del self.adyacencia[v][w]
        if not self.es_dirigido and w in self.adyacencia and v in self.adyacencia[w]:
            del self.adyacencia[w][v]

    def estan_unidos(self, v, w):
        return v in self.adyacencia and w in self.adyacencia[v]

    def peso_arista(self, v, w):
        if self.estan_unidos(v, w):
            return self.adyacencia[v][w]
        return None

    def obtener_vertices(self):
        return list(self.adyacencia.keys())

    def vertice_aleatorio(self):
        if not self.adyacencia:
            return None
        return random.choice(list(self.adyacencia.keys()))

    def adyacentes(self, v):
        if v not in self.adyacencia:
            return []
        return list(self.adyacencia[v].keys())

    def __str__(self):
        tipo = "Dirigido" if self.es_dirigido else "No dirigido"
        res = [f"Grafo {tipo} con {len(self.adyacencia)} vértices:"]
        for v in self.adyacencia:
            ady = ', '.join(f"{w} (peso: {p})" for w, p in self.adyacencia[v].items())
            res.append(f"{v} -> {ady}")
        return "\n".join(res)
