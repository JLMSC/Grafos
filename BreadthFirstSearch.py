from dataclasses import dataclass, field

from Graph import Graph


@dataclass
class BreadthFirstSearch:
    """Responsável pela Busca me Largura."""

    graph: Graph = field(repr=False)

    def apply_bfs(self, source: str) -> list[tuple[str, ...]]:
        """Realiza a Busca em Largura em um grafo.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            list[tuple[str, ...]]: O caminho percorrido pelo algoritmo, os rótulos dos vértices.
        
        Examples:
            BreadthFirstSearch(...).apply_bfs("A")

            BreadthFirstSearch(...).apply_bfs("1")
            ...
        """
        # Indica quais vértices vão ser visitados.
        queue = [source]
        # Indica quais vértices foram visitados.
        visited = [False] * self.graph.vertex_count
        # Indica o caminho percorrido pelo BFS.
        path = []
        while queue:
            # Próximo vértice a ser visitado.
            current_vertex = queue.pop(0)
            # Índice do próximo vértice.
            current_vertex_index = self.graph.translate_vertex_label_to_index(current_vertex)
            if not visited[current_vertex_index]:
                # Marca o vértice atual como visitado.
                visited[current_vertex_index] = True
                # Visita os vértices adjacentes.
                for neighbor_index, neighbor in enumerate(self.graph.vertexes):
                    if self.graph.contain_undirected_edge((current_vertex, neighbor)):
                        if not visited[neighbor_index]:
                            # Adiciona ao caminho percorrido e repete todo o processo.
                            path.append((current_vertex, neighbor))
                            queue.append(neighbor)
        return path
    
    def get_bfs_level(self, source: str) -> dict[str, int]:
        """Retorna o nível dos vértices percorrido pelo BFS.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            dict[str, int]: O nível dos vértices.
        
        Examples:
            BreadthFirstSearch(...).get_bfs_level("A")

            BreadthFirstSearch(...).get_bfs_level("1")
            ...
        """
        # Nível dos vértices.
        level = dict.fromkeys(self.graph.vertexes, 0)
        # Caminho percorrido pelo BFS.
        path = self.apply_bfs(source)
        # Atualiza o nível dos vértices.
        for edge in path:
            # Extrai o rótulo dos arcos.
            (i, j) = edge
            # Atualiza o nível.
            level[j] = level[i] + 1
        return level
    
    def get_bfs_tree(self, source: str) -> Graph:
        """Gera a Árvore Geradora do BFS.

        Args:
            source (str): O rótulo do vértice tomado como ponto de partida.

        Returns:
            Graph: A Árvore Geradora.
        
        Examples:
            BreadthFirstSearch(...).get_bfs_tree("A")

            BreadthFirstSearch(...).get_bfs_tree("1")
            ...
        """
        # Inicializa a matriz de incidência da árvore geradora.
        tree = Graph()
        # Caminho percorrido pelo BFS.
        path = self.apply_bfs(source)
        # Vértices inclusos no caminho percorrido pelo BFS.
        vertexes_in_bfs_path = self.get_bfs_vertexes(source)
        # Adiciona os vértices.
        for vertex in vertexes_in_bfs_path:
            tree.add_vertex(vertex)
        # Adiciona os arcos.
        for edge in path:
            # Custo do arco.
            cost = self.graph.get_edge_weight(edge)
            # Por fim, adiciona os arcos com os custos.
            tree.add_edge_undirected(edge)
        # Monta o grafo.
        tree.create_graph()
        # Atualiza o grafo.
        tree.update_graph()
        # Retorna o grafo.
        return tree


    def get_bfs_vertexes(self, source: str) -> list[str]:
        """Indica quais vértices foram percorridos pelo BFS.

        Args:
            source (str): O rótulo dos vértices tomado como ponto de partida.

        Returns:
            list[str]: Os vértices que foram visitados pelo BFS.

        Examples:
            BreadthFirstSearch(...).get_bfs_vertexes("A")

            BreadthFirstSearch(...).get_bfs_vertexes("1")
            ... 
        """
        # Caminho percorrido pelo BFS.
        path = self.apply_bfs(source)
        return sorted(set([vertex for edge in path for vertex in edge]))
