import random

class Grafo:
    def __init__(self, es_dirigido, lista_vertices):
        self.dic = {v:{} for v in lista_vertices}
        self.es_dirigido = es_dirigido
        self.cant = len(self.dic)

    def agregar_vertice(self, v):
        if v in self.dic:
            return
        self.dic[v] = {}
        self.cant += 1

    def eliminar_vertice(self, v):
        if v not in self.dic: 
            print("El vertice no pertenece al grafo")
            return
        self.dic.pop(v)
        for w in self.dic:
            if v in w:
                w.pop(v)
        self.cant -= 1
        
    def agregar_arista(self, v1, v2, p):
        if v1 not in self.dic or v2 not in self.dic:
            print("Un vertice no pertenece al grafo", v1, v2)
            return
        self.dic[v1][v2] = p
        if not self.es_dirigido:
            self.dic[v2][v1] = p

    def eliminar_arista(self, v1, v2):
        if v1 not in self.dic or v2 not in self.dic:
            print("Un vertice no pertenece al grafo")
            return
        self.dic[v1].pop(v2)
        if not self.es_dirigido:
            self.dic[v2].pop(v1)

    def peso(self, v1, v2):
        if v1 not in self.dic or v2 not in self.dic:
            print("Un vertice no pertenece al grafo")
            return
        return self.dic[v1][v2]
    
    def obtener_vertices(self):
        return [v for v in self.dic]
    
    def adyacentes(self, v):
        return [w for w in self.dic[v]]

    def vertice_aleatorio(self):
        return random.choice(list(self.dic.keys()))

    def contiene_arista(self, v1, v2):
        return v2 in self.dic[v1]

    def __iter__(self):
        return iter(self.dic)

    def __len__(self):
        return self.cant

