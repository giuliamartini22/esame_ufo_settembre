
from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        maxLat = 0
        minLat = 0
        maxLon = 0
        minLon = 0
        self._listShape = []
        self._grafo = nx.Graph()
        self._idMap = {}
        self._nodi = []
        self._listEdges = []

    def populateLimitiLat(self):
        lista = DAO.get_all_valori_limite()
        maxLat = float(lista[0][0])
        minLat = float(lista[0][1])
        return maxLat, minLat

    def populateLimitiLong(self):
        lista = DAO.get_all_valori_limite()
        maxLon = float(lista[0][2])
        minLon = float(lista[0][3])
        return maxLon, minLon

    def getShape(self):
        self._listShape = DAO.getAllShapes()
        return self._listShape
    def buildGraph(self, lat, long, shape):
        self._grafo.clear()
        self._nodi = DAO.get_all_states(lat, long, shape)

        for s in self._nodi:
            self._idMap[s.id] = s

        self._grafo.add_nodes_from(self._nodi)

        self._listEdges = DAO.getAllEdges(lat, long, shape)

        for e in self._listEdges:
            s1 = self._idMap[e[0]]
            s2 = self._idMap[e[1]]
            peso = e[2]
            if s1 in self._grafo.nodes and s2 in self._grafo.nodes:
                if self._grafo.has_edge(s1, s2):
                    self._grafo[s1][s2]['weight'] += peso
                else:
                    self._grafo.add_edge(s1, s2, weight=peso)

    def archiPesiMaggiori(self):
        listaArchi = []
        listaBest = []
        for uscente, entrante in self._grafo.edges():
            pesoArco = self._grafo[uscente][entrante]["weight"]
            listaArchi.append((uscente, entrante, pesoArco))
        listaArchi.sort(key=lambda x: x[2], reverse=True)
        conta = 0
        for a in range(0, len(listaArchi)):
            if conta <= 4:
                listaBest.append(listaArchi[a])
                conta = conta + 1
        return listaBest

    def archiGradiMaggiori(self):
        listaNodi = []
        listaBest = []
        for stato in self._grafo.nodes:
            grado = self._grafo.degree(stato)
            listaNodi.append((stato, grado))
        listaNodi.sort(key=lambda x: x[1], reverse=True)
        conta = 0
        for a in range(0, len(listaNodi)):
            if conta <= 4:
                listaBest.append(listaNodi[a])
                conta = conta + 1
        return listaBest

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()