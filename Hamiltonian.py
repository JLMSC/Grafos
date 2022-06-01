from copy import deepcopy
from dataclasses import dataclass, field

from Graph import Graph


@dataclass
class Hamiltonian:
    """Responsável por operações Hamiltonianas."""

    graph: Graph = field(repr=False)

    def graph_has_closure(self, degree: list[int] = list()) -> bool:
        """Verifica se existe um Fecho Hamiltoniano no grafo.

        Args:
            degree (list[int], optional): A contagem de graus do vértices.

        Returns:
            bool: Se há um Fecho Hamiltoniano no grafo.
        """
        # Usa o valor padrão dos graus, se nenhum for fornecido.
        if len(degree) == 0:
            degree = self.graph.get_vertexes_degree()
        max_edges_possible = (self.graph.vertex_count * (self.graph.vertex_count - 1)) // 2
        max_edges_in_parent = sum([v - i for i, v in enumerate(degree)])
        return max_edges_in_parent == max_edges_possible

    def is_graph_dirac(self) -> bool:
        """Aplica o Teorema de Dirac no grafo.

        Returns:
            bool: Se o grafo está de acordo com o teorema.
        """
        if self.graph.vertex_count >= 3:
            return all(
                degree > self.graph.vertex_count // 2
                for degree in self.graph.get_vertexes_degree()
            )
        return False

    def is_graph_ore(self) -> bool:
        """Aplica o Teorema de Ore no grafo.

        Returns:
            bool: Se o grafo está de acordo com o teorema.
        """
        # Grau dos vértices do grafo.
        degree = self.graph.get_vertexes_degree()
        # Itera sobre os vértices não-adjacentes.
        for i_index, i in enumerate(self.graph.vertexes):
            for j_index, j in enumerate(self.graph.vertexes):
                if i != j:
                    if not self.graph.contain_undirected_edge((i, j)):
                        # Verifica se não é possível ligar os vértices não-adjacentes.
                        if not (degree[i_index] + degree[j_index]) >= self.graph.vertex_count:
                            return False
        return True

    def is_graph_bondy(self) -> bool:
        """Aplica o Teorema de Bondy Chvatal no grafo.

        Returns:
            bool: Se o grafo está de acordo com o teorema.
        """
        
        def connect_vertexes_until() -> list[int]:
            """Conecta vértices não-adjacentes até que não seja mais possível.

            Returns:
                list[int]: O grau dos vértices do grafo.
            """
            # Grau dos vértices do grafo.
            degree = graph_copy.get_vertexes_degree()
            # Itera sobre os vértices não-adjacentes.
            for i_index, i in enumerate(graph_copy.vertexes):
                for j_index, j in enumerate(graph_copy.vertexes):
                    if i != j:
                        if not graph_copy.contain_undirected_edge((i, j)):
                            # Verifica se não é possível ligar os vértices não-adjacentes.
                            if not (degree[i_index] + degree[j_index]) >= self.graph.vertex_count:
                                # Adiciona um arco.
                                graph_copy.add_edge_undirected((i, j))
                                # Repete todo o processo.
                                return connect_vertexes_until()
            return graph_copy.get_vertexes_degree()
        
        # Cria uma cópia do grafo e aplica o teorema.
        graph_copy = deepcopy(self.graph)
        return self.graph_has_closure(connect_vertexes_until())

