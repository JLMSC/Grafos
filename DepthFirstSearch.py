from dataclasses import dataclass, field

from Graph import Graph


@dataclass
class DepthFirstSearch:
    """Responsável pela Busca em Profundidade."""

    graph: Graph = field(repr=False)

    def apply_dfs(self, source: str) -> list[tuple[str, ...]]:
        """Realiza a Busca em Profundidade em um grafo.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            list[tuple[str, ...]]: O caminho percorrido pelo algoritmo, os rótulos dos vértices.
        
        Examples:
            DepthFirstSearch(...).apply_dfs("A")

            DepthFirstSearch(...).apply_dfs("1")
            ...
        """
        
        def dfs_until(source: str):
            """Implementação recursiva do Depth-First Search.

            Args:
                source (str): O rótulo do vértice tomado como ponto de partida.
            """

            # Marca o vértice atual como visitado.
            source_index = self.graph.translate_vertex_label_to_index(source)
            visited[source_index] = True
            # Visita os vértices adjacentes.
            for neighbor_index, neighbor in enumerate(self.graph.vertexes):
                if self.graph.contain_undirected_edge((source, neighbor)):
                    if not visited[neighbor_index]:
                        # Adiciona ao caminho percorrido e repete todo o processo.
                        path.append((source, neighbor))
                        dfs_until(neighbor)

        # Indica quais vértices foram visitados.
        visited = [False] * self.graph.vertex_count
        # Indica o caminho percorrido pelo algoritmo.
        path = []
        dfs_until(source)
        return path

    def get_dfs_level(self, source: str) -> dict[str, int]:
        """Retorna o nível de profundidade dos vértices percorridos pelo DFS.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            dict[str, int]: O nível de profundidade dos vértices.
        
        Examples:
            DepthFirstSearch(...).get_dfs_level("A")

            DepthFirstSearch(...).get_dfs_level("1")
            ...
        """
        # Nível de profundidade dos vértices.
        depth = dict.fromkeys(self.graph.vertexes, 0)
        # Caminho percorrido pelo DFS.
        path = self.apply_dfs(source)
        # Atualiza o nível de profundiade dos vértices.
        for edge in path:
            # Extrai o rótulo dos arcos.
            (i, j) = edge
            # Atualiza o nível.
            depth[j] = depth[i] + 1
        return depth
    
    def get_dfs_tree(self, source: str) -> Graph:
        """Gera a Árvore de Profundidade do DFS.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            Graph: A Árvore de Profundidade.
        
        Examples:
            DepthFirstSearch(...).get_dfs_tree("A")

            DepthFirstSearch(...).get_dfs_tree("1")
            ...
        """
        # Inicializa a matriz de incidência da árvore de profundidade.
        tree = Graph()
        # Caminho percorrido pelo DFS.
        path = self.apply_dfs(source)
        # Vértices inclusos no caminho percorrido pelo DFS.
        vertexes_in_dfs_path = self.get_dfs_vertexes(source)
        # Adiciona os vértices.
        for vertex in vertexes_in_dfs_path:
            tree.add_vertex(vertex)
        # Adiciona os arcos.
        for edge in path:
            # Custo do arco.
            cost = self.graph.get_edge_weight(edge)
            # Por fim, adiciona os arcos com os custos.
            tree.add_edge_undirected(edge, cost)
        # Monta o grafo.
        tree.create_graph()
        # Atualiza o grafo.
        tree.update_graph()
        # Retorna o grafo.
        return tree

    def get_dfs_vertexes(self, source: str) -> list[str]:
        """Indica quais vértices foram percorridos pelo DFS.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            list[str]: Os vértices que foram visitados pelo DFS.
            
        Examples:
            DepthFirstSearch(...).get_dfs_vertexes("A")

            DepthFirstSearch(...).get_dfs_vertexes("1")
            ...
        """
        # Caminho percorrido pelo DFS.
        path = self.apply_dfs(source)
        return sorted(set([vertex for edge in path for vertex in edge])) 
