from grafo import Grafo
from union_find import UnionFind
from collections import deque
import heapq
import math

def obtener_ciclo_bfs(grafo):
    visitados = set()
    for v in grafo:
        if v not in visitados:
            ciclo = bfs_ciclo(grafo, v, visitados)
            if ciclo is not None:
                return ciclo
    return None

def bfs_ciclo(grafo, v, visitados):
    q = deque()
    q.appendleft(v)
    visitados.add(v)
    padre = {}
    padre[v] = None

    while not len(q) == 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w in visitados:
                print(padre)
                print(visitados)
                if w != padre[v]:
                    return reconstruir_ciclo(padre, w, v)
            else:
                q.appendleft(w)
                visitados.add(w)
                padre[w] = v

    return None

def obtener_ciclo_dfs(grafo):
    visitados = set()
    padre = {}
    for v in grafo:
        if v not in visitados:
            padre[v] = None
            visitados.add(v)
            ciclo = dfs_ciclo(grafo, v, visitados, padre)
            if ciclo is not None:
                return ciclo
    return None

def dfs_ciclo(grafo, v, visitados, padre):
    for w in grafo.adyacentes(v):
        if w in visitados:
            if w != padre[v]:   # Esto es para grafos no dirigidos
               return reconstruir_ciclo(padre, w, v)
            #return reconstruir_ciclo(padre, w, v)

        else:
            visitados.add(w)
            padre[w] = v
            ciclo = dfs_ciclo(grafo, w, visitados, padre)
            if ciclo is not None:
                return ciclo
    return None

def reconstruir_ciclo(padre, inicio, fin):
    v = fin
    camino = []
    while v != inicio:
        camino.append(v)
        v = padre[v]
    camino.append(inicio)
    return camino[::-1]

def grados(grafo):
    visitados = set()
    g = {}
    for v in grafo:
        g[v] = {"in":0, "out":0}
    for v in grafo:
        for w in grafo.adyacentes(v):
            if w not in visitados:
                g[w]["in"] += 1
                g[v]["out"] += 1
    return g

def es_conexo(grafo):
    total = 0
    for v in grafo:
        total += 1
    
    v = grafo.vertice_aleatorio()
    q = deque()
    visitados = set()
    q.appendleft(v)
    visitados.add(v)
    while len(q) > 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                q.appendleft(w)
    return total == len(visitados)

def es_arbol(grafo):
    return aristas(grafo) == vertices(grafo)-1 and obtener_ciclo_dfs(grafo) is None and es_conexo(grafo)

def aristas(grafo):
    cant = 0
    visitados = set()
    for v in grafo:
        visitados.add(v)
        for w in grafo.adyacentes(v):
            if w not in visitados:
                cant += 1
                visitados.add(w)    
    return cant

def vertices(grafo):
    cant = 0
    for v in grafo:
        cant += 1
    return cant

def transponer(grafo):
    nuevo_grafo = Grafo(es_dirigido=True, lista_vertices=grafo.obtener_vertices())
    visitados = set()
    for v in grafo:
        visitados.add(v)
        for w in grafo.adyacentes(v):
            if w not in visitados:
                nuevo_grafo.agregar_arista(w, v, grafo.peso(v, w))
                visitados.add(w)
    return nuevo_grafo

def cumple_teoria_6_grados(grafo):
    for v in grafo:
        if not cumple_teoria_bfs(grafo, v):
            return False
    return True

def cumple_teoria_bfs(grafo, v):
    visitados = set()
    distancia = {}
    q = deque()
    visitados.add(v)
    distancia[v] = 0
    q.appendleft(v)

    while len(q) > 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                if distancia[v] == 5:
                    return False
                distancia[w] = distancia[v] + 1
                q.appendleft(w)
    return True

def recorrido_museo(grafo):
    visitados = []
    for v in grafo:
        if v not in visitados:
            _recorrido_museo(grafo, v, visitados)
    return visitados

def _recorrido_museo(grafo, v, visitados):
    visitados.append(v)
    for w in grafo.adyacentes(v):
        if w not in visitados:
            _recorrido_museo(grafo, w, visitados)

def es_bipartito(grafo):
    colores = {}
    for v in grafo:
        if v not in colores:
            if not _es_bipartito(grafo, v, colores):
                return False
    return True

def _es_bipartito(grafo, v, colores):
    colores[v] = 0
    q = deque()
    q.appendleft(v)

    while len(q) > 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w not in colores:
                colores[w] = 1 - colores[v]
                q.appendleft(w)
            else: 
                if colores[w] == colores[v]:
                    return False
    return True

def vertices_a_distancia(grafo, origen, n):
    q = deque()
    distancia, distancia_n = {}, []
    q.appendleft(origen)
    distancia[origen] = 0
    while len(q) > 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w not in distancia:
                distancia[w] = distancia[v] + 1
                if distancia[w] == n:
                    distancia_n.append(w)
                    continue
                q.appendleft(w)
    return distancia_n

def puede_ser_no_dirigido(grafo):
    for v in grafo:
        for w in grafo.adyacentes(v):
            if v not in grafo.adyacentes(w):
                return False
    return True

def orden_historia(grafo):
    gr_ent = {}
    resultado = []
    q = deque()
    for v in grafo:
        gr_ent[v] = 0
    for v in grafo:
        for w in grafo.adyacentes(v):
            gr_ent[w] += 1
    for v in grafo:
        if gr_ent[v] == 0:
            q.appendleft(v)
    while len(q) > 0:
        v = q.pop()
        resultado.append(v)
        for w in grafo.adyacentes(v):
            gr_ent[w] -= 1
            if gr_ent[w] == 0:
                q.appendleft(w)
    return resultado

def matriz_adyacencia(grafo):
    matriz = []
    for v1 in grafo:
        fila = []
        for v2 in grafo:
            if v2 in grafo.adyacentes(v1):
                fila.append(1)
            else:
                fila.append(0)
        matriz.append(fila)
    return matriz

def vertices_grado_impar_es_par(grafo):
    grados = {}
    vertices_grado_impar = []
    for v in grafo:
        grados[v] = grados.get(v, 0) + len(grafo.adyacentes(v))
    for vertice in grados:
        if grados[vertice] % 2 != 0:
            vertices_grado_impar.append(vertice)
    return len(vertices_grado_impar) % 2 == 0

def menor_cant_operaciones(x, y):
    grafo = Grafo(es_dirigido=True, lista_vertices=list(range(x, y + 1)))
    if y not in grafo:
        return "No es posible conectar x con y"
    
    for v in grafo:
        if v*2 in grafo:
            grafo.agregar_arista(v, v*2, 0)
        if v-1 in grafo:
            grafo.agregar_arista(v, v-1, 0)
    
    q = deque()
    cant = {}
    q.appendleft(x)
    cant[x] = 0

    while len(q) > 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w not in cant:
                cant[w] = cant[v] + 1
                q.appendleft(w)
    
    return cant[y]

def idioma_alien(palabras):
    grafo = grafo_desde_palabras(palabras)
    grados = {}
    for v in grafo:
        for w in grafo.adyacentes(v):
            grados[w] = grados.get(w, 0) + 1
    q = deque()
    for v in grafo:
        if v not in grados:
            print(v)
            q.appendleft(v)
    result = []
    while len(q) > 0:
        v = q.pop()
        result.append(v)
        for w in grafo.adyacentes(v):
            grados[w] -= 1
            if grados[w] == 0:
                q.appendleft(w)
    
    return result

def grafo_desde_palabras(palabras):
    grafo = Grafo(es_dirigido=True, lista_vertices=[])
    for i in range(len(palabras) - 1):
        p1 = palabras[i]
        p2 = palabras[i+1]

        for letra in p1:
            grafo.agregar_vertice(letra)
        
        for j in range(len(p1)):
            if p1[j] != p2[j]:
                grafo.agregar_vertice(p2[j])
                grafo.agregar_arista(p1[j], p2[j], 0)
                break
    return grafo

def cant_debilmente_conexas(grafo):
    componentes = {}
    visitados = set()
    for v in grafo:
        if v not in visitados:
            _cant_debilmente_conexas(grafo, v, visitados, componentes)
    return len(componentes)

def _cant_debilmente_conexas(grafo, v, visitados, componentes):
    q = deque()
    original = v
    visitados.add(original)
    componentes[original] = [original]
    q.appendleft(original)
    while len(q) > 0:
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                componentes[original].append(w)
                q.appendleft(w)
    
def rompen_el_ecosistema(grafo):
    gr_ent, gr_sal = grados_de_entrada_salida(grafo)
    vertices_rompen = set()
    for v in grafo:
        for w in grafo.adyacentes(v):
            if gr_ent[w] == 1:
                vertices_rompen.add(v)
            if gr_sal[v] == 1:
                vertices_rompen.add(w)
    return vertices_rompen

def grados_de_entrada_salida(grafo):
    gr_ent, gr_sal = {}, {}
    for v in grafo:
        gr_ent[v], gr_sal[v] = 0, 0
    for v in grafo:
        for w in grafo.adyacentes(v):
            gr_ent[w] += 1
            gr_sal[v] += 1
    return gr_ent, gr_sal

def camino_minimo_dijkstra(grafo, origen):
    distancia = {}
    padre = {}
    q = []
    for v in grafo:
        distancia[v] = math.inf
    distancia[origen] = 0
    padre[origen] = None
    heapq.heappush(q, (0, origen))
    while len(q) > 0:
        v, _ = heapq.heappop(q)
        for w in grafo.adyacentes(v):
            if (distancia[v] + grafo.peso(v, w) < distancia[w]):
                distancia[w] = distancia[v] + grafo.peso(v, w)
                padre[w] = v
                heapq.heappush(q, (distancia[w], w))
    return padre,distancia

def obtener_aristas(grafo):
    aristas = []
    for v in grafo:
        for w in grafo.adyacentes(v):
            aristas.append((v, w, grafo.peso(v,w)))
    return aristas

def camino_minimo_bf(grafo, origen):
    distancia = {}
    padre = {}
    for v in grafo:
        distancia[v] = math.inf
    distancia[origen] = 0
    padre[origen] = None
    aristas = obtener_aristas(grafo)
    for i in range(len(grafo)):
        cambio = False
        for origen, destino, peso in aristas:
            if distancia[origen] + peso < distancia[destino]:
                cambio = True
                distancia[destino] = distancia[origen] + peso
                padre[destino] = origen
        if not cambio:
            break
    for v, w, peso in aristas:
        if distancia[v] + peso < distancia[w]:
            return "Hay un ciclo negativo"
    return padre, distancia

def arbol_tendido_minimo_prim(grafo):
    origen = grafo.vertice_aleatorio()
    arbol = Grafo(es_dirigido=False, lista_vertices=grafo.obtener_vertices())
    visitados = set()
    visitados.add(origen)
    q = []
    for w in grafo.adyacentes(origen):
        heapq.heappush(q, (grafo.peso(origen, w), origen, w))
    while len(q) > 0:
        peso, origen, destino = heapq.heappop(q)
        if destino in visitados:
            continue
        visitados.add(destino)
        arbol.agregar_arista(origen, destino, peso)
        for w in grafo.adyacentes(destino):
            if w not in visitados:
                heapq.heappush(q, (grafo.peso(destino, w), destino, w))
    return arbol

PESO = 2

def arbol_tendido_minimo_kruskal(grafo):
    conjuntos = UnionFind(grafo.obtener_vertices())
    aristas = sorted(obtener_aristas(grafo), key=lambda arista: arista[PESO])
    arbol = Grafo(False, grafo.obtener_vertices())
    for a in aristas:
        v, w, peso = a
        if conjuntos.find(v) == conjuntos.find(w):
            continue
        arbol.agregar_arista(v, w, peso)
        conjuntos.union(v, w)
    return arbol


grafo = Grafo(es_dirigido=False, lista_vertices=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "Ñ", "O", "P", "X", "Y", "Z"])
grafo.agregar_arista("A", "B", 1)
grafo.agregar_arista("A", "J", 1)
grafo.agregar_arista("A", "H", 1)
grafo.agregar_arista("A", "G", 1)
grafo.agregar_arista("H", "I", 1)
grafo.agregar_arista("I", "B", 1)
grafo.agregar_arista("F", "B", 1)
grafo.agregar_arista("B", "C", 1)
grafo.agregar_arista("E", "F", 1)
grafo.agregar_arista("C", "E", 1)
grafo.agregar_arista("C", "D", 1)
grafo.agregar_arista("J", "K", 1)
grafo.agregar_arista("J", "Ñ", 1)
grafo.agregar_arista("K", "L", 1)
grafo.agregar_arista("L", "M", 1)
grafo.agregar_arista("Ñ", "O", 1)
grafo.agregar_arista("M", "N", 1)
grafo.agregar_arista("X", "Y", 1)
grafo.agregar_arista("Z", "Y", 1)
grafo.agregar_arista("X", "Z", 1)


grafo2 = Grafo(es_dirigido=True, lista_vertices=["A", "B", "C"])
grafo2.agregar_arista("A", "B", 0)
grafo2.agregar_arista("B", "A", 0)


grafo3 = Grafo(es_dirigido=True, lista_vertices=[1,2,3,4,5])
grafo3.agregar_arista(1,2,0)
grafo3.agregar_arista(2,1,0)
grafo3.agregar_arista(1,5,0)
grafo3.agregar_arista(5,1,0)
grafo3.agregar_arista(2,3,0)
grafo3.agregar_arista(3,2,0)
grafo3.agregar_arista(2,4,0)
grafo3.agregar_arista(4,2,0)


grafo4 = Grafo(es_dirigido=False, lista_vertices=[1,2,3,4,5])
grafo4.agregar_arista(1,2,0)
grafo4.agregar_arista(1,4,0)
grafo4.agregar_arista(2,5,0)
grafo4.agregar_arista(2,3,0)


grafo5 = Grafo(es_dirigido=True, lista_vertices=[1,2,3,4,5,6])
grafo5.agregar_arista(1,2,0)
grafo5.agregar_arista(1,3,0)
grafo5.agregar_arista(1,4,0)
grafo5.agregar_arista(2,3,0)
grafo5.agregar_arista(2,5,0)
grafo5.agregar_arista(3,4,0)
grafo5.agregar_arista(4,6,0)


grafo6 = Grafo(es_dirigido=False, lista_vertices=["A","B","C","D","E","F"])
grafo6.agregar_arista("A","B",7)
grafo6.agregar_arista("A","C",5)
grafo6.agregar_arista("A","E",3)
grafo6.agregar_arista("A","F",8)
grafo6.agregar_arista("B","E",1)
grafo6.agregar_arista("B","F",3)
grafo6.agregar_arista("C","D",5)
grafo6.agregar_arista("C","E",3)
grafo6.agregar_arista("C","F",2)
grafo6.agregar_arista("D","E",2)


grafo7 = Grafo(es_dirigido=True, lista_vertices=["A","B","C","D","E","F","G","H"])
grafo7.agregar_arista("A","D",-4)
grafo7.agregar_arista("A","C",-1)
grafo7.agregar_arista("A","F",3)
grafo7.agregar_arista("A","G",-5)
grafo7.agregar_arista("B","A",1)
grafo7.agregar_arista("C","G",-1)
grafo7.agregar_arista("C","H",5)
grafo7.agregar_arista("D","F",1)
grafo7.agregar_arista("D","H",8)
grafo7.agregar_arista("F","B",1)
grafo7.agregar_arista("G","C",2)
grafo7.agregar_arista("G","E",3)


grafo8 = Grafo(es_dirigido=False, lista_vertices=["A","B","C","D","E","F","G"])
grafo8.agregar_arista("A", "B", 3)
grafo8.agregar_arista("A", "D", 6)
grafo8.agregar_arista("A", "E", 4)
grafo8.agregar_arista("B", "C", 2)
grafo8.agregar_arista("B", "D", 4)
grafo8.agregar_arista("C", "D", 4)
grafo8.agregar_arista("C", "E", 5)
grafo8.agregar_arista("C", "F", 3)
grafo8.agregar_arista("D", "E", 3)
grafo8.agregar_arista("E", "F", 10)
grafo8.agregar_arista("F", "G", 6)

arbol = arbol_tendido_minimo_prim(grafo8)
for v in arbol:
    print(v, arbol.adyacentes(v))

arbol2 = arbol_tendido_minimo_kruskal(grafo8)
for v in arbol2:
    print(v, arbol2.adyacentes(v))