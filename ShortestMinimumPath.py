from copy import copy
from dataclasses import dataclass, field

from Graph import Graph


@dataclass
class ShortestMinimumPath:
    """Responsável pelos algoritmos de caminho mínimo."""

    graph: Graph = field(repr=False)

    def apply_dijkstra_algorithm(self, source: str) -> dict[str, list[float] | list[str] | dict[str, str]]:
        """Aplica o algoritmo, de Dijkstra, de caminho mínimo, no grafo.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            dict[str, list[float] | list[str] | dict[str, str]]: O custo, antecessores e o caminho percorrido.

        Examples:
            ShortestMinimumPath(...).apply_dijkstra_algorithm("A")

            ShortestMinimumPath(...).apply_dijkstra_algorithm("1")
            ...
        """
        # Inicializa o custo dos vértices.
        distance = [float("inf")] * self.graph.vertex_count
        # Inicializa os vértices antecessores.
        previous = dict.fromkeys(self.graph.vertexes, "")
        # Indica o caminho percorrido pelo algoritmo.
        path = []
        # Indica os vértices a serem visitados.
        queue = copy(self.graph.vertexes)

        # Define o custo do vértice do ponto de partida.
        distance[self.graph.translate_vertex_label_to_index(source)] = 0

        # Percorre todos os vértices do grafo.
        while queue:
            # Pega o vértice, que não foi visitado, com o menor custo.
            remaining_cost = [
                cost 
                for vertex, cost in enumerate(distance) 
                if self.graph.translate_vertex_index_to_label(vertex) in queue
            ]
            next_vertex = queue.pop(remaining_cost.index(min(remaining_cost)))
            next_vertex_index = self.graph.translate_vertex_label_to_index(next_vertex)

            # Adiciona ao caminho percorrido.
            if distance[next_vertex_index] != float("inf"):
                path.append(next_vertex)
            
            # Pega todos os seus vizinhos e atualiza o custo e os antecessores.
            for neighbor_index, neighbor in enumerate(self.graph.vertexes):
                if self.graph.contain_directed_edge((next_vertex, neighbor)):
                    # O novo custo, desde a origem, do vértice.
                    new_cost = distance[next_vertex_index] + self.graph.get_edge_weight((next_vertex, neighbor))
                    # Atualiza o custo e o antecessor se for menor.
                    if new_cost < distance[neighbor_index]:
                        distance[neighbor_index] = new_cost
                        previous[neighbor] = next_vertex

        # Organiza o caminho percorrido pelo algoritmo.
        organized_path = []
        for vertex in path:
            if vertex not in organized_path:
                organized_path.append(vertex)
        return {
            "Custo dos vértices": distance, 
            "Antecessores": previous, 
            "Caminho Percorrido": path
        }
    
    def apply_bellman_ford_algorithm(self, source: str) -> dict[str, list[float] | dict[str, str] | str]:
        """Aplica o algoritmo, de Bellman-Ford, de caminho mínimo, no grafo.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            dict[str, list[float] | dict[str, str]]: Os custos, antecessores e a ordem de relaxamento.
        
        Examples:
            ShortestMinimumPath(...).apply_bellman_ford_algorithm("A")

            ShortestMinimumPath(...).apply_bellman_ford_algorithm("1")
            ...
        """
        
        def relax(source: str, destiny: str, cost: int):
            """Aplica a técnica de relaxamento em um arco.

            Args:
                source (str): O rótulo do vértice tomado como ponto de partida.
                destiny (str): O rótulo do vértice tomado como destino.
                cost (int): O custo do arco.
            """
            # Converte o rótulo dos vértices para o índice.
            source_index, destiny_index = map(
                self.graph.translate_vertex_label_to_index, (source, destiny)
            )
            # Atualiza o custo e o antecessor, caso seja possível.
            if distance[destiny_index] > distance[source_index] + cost:
                distance[destiny_index] = distance[source_index] + cost
                previous[destiny] = source
                relaxing_order.append((source, destiny))

        def find_cycles() -> bool:
            """Procura por ciclos no grafo.

            Returns:
                bool: Retorna verdadeiro caso exista um ciclo no grafo.
            """
            # Itera sobre todos os arcos.
            for u_index, u in enumerate(self.graph.vertexes):
                for v_index, v in enumerate(self.graph.vertexes):
                    # Verifica se existe um arco nos vértices 'u' e 'v'.
                    if self.graph.contain_directed_edge((u, v)):
                        # Se ainda for possível atualizar um custo, um ciclo existe no grafo.
                        if distance[v_index] > distance[u_index] + self.graph.get_edge_weight((u, v)):
                            return True
            return False

        # Inicializa o custo dos vértices.
        distance = [float("inf")] * self.graph.vertex_count
        # Inicializa os vértices antecessores.
        previous = dict.fromkeys(self.graph.vertexes, "")
        # Ordem de relaxamento dos arcos.
        relaxing_order = []

        # Define o custo do vértice do ponto de partida.
        distance[self.graph.translate_vertex_label_to_index(source)] = 0

        # Itera sobre todos os arcos.
        for _ in range(1, self.graph.vertex_count):
            for u in self.graph.vertexes:
                for v in self.graph.vertexes:
                    # Verifica se existe um arco nos vértices 'u' e 'v'.
                    if self.graph.contain_directed_edge((u, v)):
                        # Aplica a técnica de relaxamento no arco.
                        relax(u, v, self.graph.get_edge_weight((u, v)))

        # Procura por ciclos no grafo.
        if find_cycles():
            return {
                "Custo dos vértices": "Nenhum, um ciclo foi encontrado.", 
                "Antecessores": "Nenhum, um ciclo foi encontrado.",
                "Ordem de relaxamento": "Nenhum, um ciclo foi encontrado."
            }
        else:
            return {
                "Custo dos vértices": distance, 
                "Antecessores": previous, 
                "Ordem de relaxamento": relaxing_order
            }

    def apply_floyd_warshall_algorithm(self) -> dict[str, list[list[float]] | list[list[str]]]:
        """Aplica o algoritmo, de Floyd-Warshall, para todos os arcos.

        Returns:
            dict[str, list[list[float]] | list[list[str]]]: Os custos e os antecessores.

        Examples:
            ShortestMinimumPath(...).apply_floyd_warshall_algorithm()
            ...
        """

        # Cria a matriz de incidência, por padrão, com custos infinitos.
        distance = [    # Custos dos arcos.
            [float("inf") for _ in range(self.graph.vertex_count)]
            for _ in range(self.graph.vertex_count)
        ]
        # Cria a matriz de incidência, por padrão, com antecessores nulos.
        previous = [    # Antecessores.
            ["" for _ in range(self.graph.vertex_count)]
            for _ in range(self.graph.vertex_count)
        ]

        # Atualiza os custos da matriz de incidência.
        # Junto com os antecessores.
        for i in range(self.graph.vertex_count):
            distance[i][i] = 0
            previous[i][i] = self.graph.translate_vertex_index_to_label(i)

        # Percorre todos os arcos do grafo.
        for (i, j) in self.graph.edges:
            # Transforma para o rótulo para o índice.
            i_index, j_index = map(self.graph.translate_vertex_label_to_index, (i, j))
            # Adiciona o custo do arco ao custo.
            distance[i_index][j_index] = self.graph.get_edge_weight((i, j))
            # Adiciona o antecessor do arco.
            previous[i_index][j_index] = j
        
        # Atualiza o custo dos arcos, para menor, se possível, percorrendo "k" vértices.
        for k in range(self.graph.vertex_count):
            for i in range(self.graph.vertex_count):
                for j in range(self.graph.vertex_count):
                    # Verifica se o novo custo é menor que o existente.
                    if distance[i][j] > distance[i][k] + distance[k][j]:
                        # Atualiza o custo para menor.
                        distance[i][j] = distance[i][k] + distance[k][j]
                        # Atualiza o antecessor.
                        previous[i][j] = previous[i][k]
        
        # Retorna o menor custo possível dos arcos e os antecessores.
        return {
            "Custo dos Arcos": distance,
            "Vértices Antecessores": previous
        }
