from copy import deepcopy
from dataclasses import dataclass, field
from random import choice

from DepthFirstSearch import DepthFirstSearch
from Graph import Graph


@dataclass
class Euler:
    """Responsável por operações Eulerianas."""

    graph: Graph = field(repr=False)

    def is_graph_euler(self) -> bool:
        """Verifica se o grafo está de acordo com o Teorema de Euler.

        Returns:
            bool: Se o grafo está de acordo com o Teorema de Euler.
        """
        return all(
            degree % 2 == 0 for degree in self.graph.get_vertexes_degree()
        )
    
    def is_graph_semi_euler(self) -> bool:
        """Verifica se o grafo está de acordo com o Teorema Semi-Euleriano.

        Returns:
            bool: Se o grafo está de acordo com o Teorema de Semi-Euleriano.
        """
        return [
            degree % 2 != 0 for degree in self.graph.get_vertexes_degree()
        ].count(True) == 2

    def get_euler_circuit(self) -> dict[str, list[tuple[str, ...] | int]]:
        """Gera o circuito euleriano de um grafo, caso o grafo seja euleriano ou semi-euleriano.

        Returns:
            dict[str, list[tuple[str, ...] | int]]: As informações do circuito euleriano.
        """

        def is_a_bridge(source: str, destiny: str) -> bool:
            """Verifica se um arco é uma ponte.

            Args:
                source (str): O rótulo do vértice tomado como ponto de partida.
                destiny (str): O rótulo do vértice tomado como destino.

            Returns:
                bool: Se o arco é uma ponte.
            """
            # Conserva o custo do arco, pois o arco será adicionado a seguir.
            edge_cost = graph_copy.get_edge_weight((source, destiny))
            # Remove o arco, para verificação de pontes.
            graph_copy.remove_edge_undirected((source, destiny))
            # Vértices percorridos pelo DFS.
            vertexes_in_dfs_path = dfs.get_dfs_vertexes(source)
            # Adiciona o arco removido, com o seu custo original.
            graph_copy.add_edge_undirected((source, destiny), edge_cost)
            # Inidica se todos os vértices do grafo foram visitados.
            visited_vertexes = [vertex in vertexes_in_dfs_path for vertex in graph_copy.vertexes]
            # Atualiza o grau dos vértices do grafo, pois arcos serão removidos.
            degree = graph_copy.get_vertexes_degree()
            # Marca os vértices que não possuem arcos como visitados.
            for index, vertex_degree in enumerate(degree):
                if not vertex_degree:
                    visited_vertexes[index] = True
            return all(visited_vertexes)

        def is_path_valid(source: str, destiny: str) -> bool:
            """Verifica se o próximo vértice, o destino, é um caminho válido.

            Args:
                source (str): O rótulo do vértice tomado como ponto de partida.
                destiny (str): O rótulo do vértice tomado como destino.

            Returns:
                bool: Se o próximo vértice, ou seja o destino, é um caminho válido.
            """
            # Atualiza o grau dos vértices do grafo, pois arcos serão removidos.
            degree = graph_copy.get_vertexes_degree()
            if degree[graph_copy.translate_vertex_label_to_index(source)] != 1:
                return is_a_bridge(source, destiny)
            return True

        def get_next_valid_path(source: str) -> dict[str, list[tuple[str, ...] | int]]:
            """Percorre todos os vértices, verificando os arcos 
            e escolhendo aquele que é válido.

            Args:
                source (str): O rótulo do vértice tomado como ponto de partida.
            
            Returns:
                dict[str, list[tuple[str, ...] | int]]: As informações do circuito euleriano.
            """
            for vertex in graph_copy.vertexes:
                if graph_copy.contain_undirected_edge((source, vertex)):
                    if is_path_valid(source, vertex):
                        # Adiciona as informações do circuito euleriano.
                        euler_circuit["Caminho Euleriano"].append((source, vertex))
                        euler_circuit["Custo do Caminho"].append(graph_copy.get_edge_weight((source, vertex)))
                        # Remove o arco.
                        graph_copy.remove_edge_undirected((source, vertex))
                        # Repete todo o processo.
                        return get_next_valid_path(vertex)
            return euler_circuit

        # Define as informações do circuito euleriano.
        euler_circuit = {"Caminho Euleriano": [], "Custo do Caminho": []}

        # Copia o grafo e a contagem de graus dos vértices.
        graph_copy = deepcopy(self.graph)
        degree = graph_copy.get_vertexes_degree()

        # Inicializa a classe DFS.
        dfs = DepthFirstSearch(graph_copy)

        # Define o ponto de partida.
        if self.is_graph_euler():
            return get_next_valid_path(choice(graph_copy.vertexes))
        elif self.is_graph_semi_euler():
            valid_source = list(filter(lambda x: x % 2 != 0, degree))
            return get_next_valid_path(
                graph_copy.translate_vertex_index_to_label(
                    valid_source.index(choice(valid_source))
                )
            )
        else:
            raise ValueError("O grafo não é euleriano ou semi-euleriano.")
