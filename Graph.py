from collections import Counter
from dataclasses import dataclass, field
from json import load
from os.path import exists

# TODO: Método ToString ???? Tem o REPR do dataclass, só precisa pro grafo.


@dataclass
class Graph:
    """Representa um Grafo."""

    graph: list[list[int]] = field(repr=False, init=False, default_factory=list)
    vertexes: list[str] = field(init=False, default_factory=list)
    vertex_count: int = field(init=False, default_factory=int)
    edges: dict[tuple[str, str], int] = field(init=False, default_factory=dict)

    def recreate_graph(self):
        """Recria o grafo, a matriz de incidência."""
        self.create_graph()

    def create_graph(self):
        """Cria uma nova matriz de incidência para o grafo."""
        self.graph = [
            [0 for _ in range(len(self.vertexes))] for _ in range(len(self.vertexes))
        ]

    def update_graph(self):
        """Atualiza o grafo, adicionando novos arcos."""
        if len(self.graph) > 0:
            # Percorre todos os arcos existentes.
            for edge, weight in self.edges.items():
                # Pega ambos os vértices, porém, somente o seus índices.
                (i, j) = map(self.translate_vertex_label_to_index, edge)
                # Adiciona o arco no grafo.
                self.graph[i][j] = weight
        else:
            self.create_graph()

    def create_graph_from_file(self, file_path: str):
        """Cria um grafo a partir de um arquivo lido (*.json)

        Args:
            file_path (str): O caminho do arquivo.

        Examples:
            Graph().create_graph_from_file("Arquivo.json")

            Graph().create_graph_from_file("Grafo.json")
            ...
        """

        # Verifica se o arquivo existe.
        if exists(file_path):
            # Tenta abrir o arquivo, caso seja encontrado.
            try:
                with open(f"{file_path}", "r", encoding="utf-8") as file:
                    # Pega o conteúdo do arquivo .json
                    data = load(file)

                    # Adiciona os vértices.
                    self.add_vertexes(tuple(map(str, data["Vertexes"][0])))

                    # Adiciona os arcos.
                    for i, j, *w in data["Edges"]:
                        if len(w) > 1:
                            raise ValueError(
                                "O formato dos arcos do arquivo lido é inválido"
                            )
                        self.add_edge_directed((i, j), w[0] if w else 1)

                    # Fecha o arquivo após a sua utilização.
                    file.close()
            except FileNotFoundError:
                raise FileNotFoundError("O arquivo não foi encontrado.")
        else:
            raise FileExistsError("O arquivo não existe.")

    def add_vertex(self, vertex: str):
        """Adiciona um vértice ao grafo.

        Args:
            vertex (str): O rótulo do vértice a ser adicionado.

        Examples:
            Graph().add_vertex("1")

            Graph().add_vertex("A")
            ...
        """
        if not self.contain_vertex(vertex):
            self.vertexes.append(vertex)
            self.vertex_count += 1
            self.recreate_graph()
        else:
            raise ValueError("O vértice a ser adicionado já existe no grafo.")
        
    def remove_vertex(self, vertex: str):
        """Remove um vértice do grafo.

        Args:
            vertex (str): O rótulo do vértice a ser removido.

        Examples:
            Graph().remove_vertex("1")

            Graph().remove_vertex("A")
            ...
        """
        if self.contain_vertex(vertex):
            # Remove todos os arcos que contém tal vértice.
            for v in self.vertexes:
                self.remove_edge_undirected((vertex, v))
            # Remove o vértice do grafo.
            self.vertexes.remove(vertex)
            self.vertex_count -= 1
            # Recria o grafo.
            self.recreate_graph()
            # Atualiza o grafo.
            self.update_graph()
        else:
            raise ValueError("O vértice a ser removido não existe.")

    def add_vertexes(self, vertexes: tuple[str, ...]):
        """Adiciona múltiplos vértices ao grafo.

        Args:
            vertexes (tuple[str, ...]): Os rótulos dos vértices a serem adicionados.

        Examples:
            Graph().add_vertexes(("1", "2", "3"))

            Graph().add_vertexes(("A", "B", "C"))
            ...
        """
        if not self.contain_vertexes(vertexes):
            for vertex in vertexes:
                # Adiciona os vértices do grafo.
                self.vertexes.append(vertex)
                self.vertex_count += 1
            self.recreate_graph()
        else:
            raise ValueError("Algum vértice a ser adicionado já existe no grafo.")
    
    def remove_vertexes(self, vertexes: tuple[str, ...]):
        """Remove múltiplos vértices do grafo.

        Args:
            vertexes (tuple[str, ...]): Os rótulos dos vértices a serem removidos.

        Examples:
            Graph().remove_vertexes(("1", "2", "3"))

            Graph().remove_vertexes(("A", "B", "C"))
            ...
        """
        if self.contain_vertexes(vertexes):
            for vertex in vertexes:
                # Remove todos os arcos que contém tais vértice.
                for v in self.vertexes:
                    self.remove_edge_undirected((vertex, v))
                # Remove os vértices do grafo.
                self.vertexes.remove(vertex)
                self.vertex_count -= 1
            # Recria o grafo.
            self.recreate_graph()
            # Atualiza o grafo.
            self.update_graph()
        else:
            raise ValueError("Algum vértice a ser removido não existe no grafo.")

    def contain_vertex(self, vertex: str) -> bool:
        """Verifica se um vértice está no grafo.

        Args:
            vertex (str): O rótulo do vértice a ser procurado.

        Returns:
            bool: Se o vértice existe no grafo.

        Examples:
            Graph().contain_vertex("1")

            Graph().contain_vertex("A")
            ...
        """
        return vertex in self.vertexes

    def contain_vertexes(self, vertexes: tuple[str, ...]) -> bool:
        """Verifica se múltiplos vértices estão no grafo.

        Args:
            vertexes (tuple[str, ...]): Os rótulos dos vértices a serem procurados.

        Returns:
            bool: Se os vértices existem no grafo.

        Examples:
            Graph().contain_vertexes(("1", "2", "3"))

            Graph().contain_vertexes(("A", "B", "C"))
            ...
        """
        return all([v in self.vertexes for v in vertexes])

    def add_edge_directed(self, edge: tuple[str, ...], weight: int = 1):
        """Adiciona um arco direcionado ao grafo.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices no qual será criado o arco.
            weight (int, optional): O peso do arco, se nenhum valor for fornecido, o peso será 1.

        Examples:
            Graph().add_edge(("1", "2"), 3)

            Graph().add_edge(("A", "B"))
            ...
        """
        # Verifica se é um arco apropriado.
        if len(edge) == 2:
            # Verifica se os rótulos existem no grafo.
            if self.contain_vertexes(edge):
                # Adiciona o arco direcionado.
                self.edges[edge] = weight
                # Atualiza o grafo.
                self.update_graph()
            else:
                raise ValueError("Os rótulos fornecidos não existem no grafo.")
        else:
            raise ValueError("O tamanho do arco não é válido.")
    
    def remove_edge_directed(self, edge: tuple[str, ...]):
        """Remove um arco direcionado do grafo.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices no qual será removido o arco.
        
        Examples:
            Graph().remove_edge_directed(("1", "2"))

            Graph().remove_edge_directed(("A", "B"))
            ...
        """
        # Verifica se é um arco apropriado.
        if len(edge) == 2:
            # Verifica se os rótulos existem no grafo.
            if self.contain_vertexes(edge):
                # Verifica se o arco existe no grafo.
                if self.contain_directed_edge(edge):
                    # Remove o arco.
                    self.edges.pop(edge)
                    # Recria o grafo.
                    self.recreate_graph()
                    # Atualiza o grafo.
                    self.update_graph()
            else:
                raise ValueError("Os rótulos fornecidos não existem no grafo.")
        else:
            raise ValueError("O tamanho do arco não é válido.")

    def add_edge_undirected(self, edge: tuple[str, ...], weight: int = 1):
        """Adiciona um arco não-direcionado ao grafo.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices no qual será criado o arco.
            weight (int, optional): O peso do arco, se nenhum valor for fornecido, o peso será 1.

        Examples:
            Graph().add_edge(("1", "2"), 3)

            Graph().add_edge(("A", "B"))
            ...
        """
        # Verifica se é um arco apropriado.
        if len(edge) == 2:
            # Verifica se os rótulos existem no grafo.
            if self.contain_vertexes(edge):
                # Adiciona o arco não-direcionado.
                self.edges[edge] = weight
                self.edges[tuple(reversed(edge))] = weight
                # Atualiza o grafo.
                self.update_graph()
            else:
                raise ValueError("Os rótulos fornecidos não existem no grafo.")
        else:
            raise ValueError("O tamanho do arco não é válido.")
    
    def remove_edge_undirected(self, edge: tuple[str, ...]):
        """Remove um arco não-direcionado do grafo.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices no qual será removido o arco.
        
        Examples:
            Graph().remove_edge_undirected(("1", "2"))

            Graph().remove_edge_undirected(("A", "B"))
            ...
        """
        # Verifica se é um arco apropriado.
        if len(edge) == 2:
            # Verifica se os rótulos existem no grafo.
            if self.contain_vertexes(edge):
                # Verifica se o arco existe no grafo.
                if self.contain_undirected_edge(edge):
                    # Remove o arco.
                    self.edges.pop(edge)
                    self.edges.pop(tuple(reversed(edge)))
                    # Recria o grafo.
                    self.recreate_graph()
                    # Atualiza o grafo.
                    self.update_graph()
            else:
                raise ValueError("Os rótulos fornecidos não existem no grafo.")
        else:
            raise ValueError("O tamanho do arco não é válido.")

    def contain_directed_edge(self, edge: tuple[str, ...]) -> bool:
        """Verifica se um arco está no grafo.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices, ou seja, o arco.

        Returns:
            bool: Se o arco existe no grafo.

        Examples:
            Graph().contain_directed_edge(("1", "2"))

            Graph().contain_directed_edge(("A", "C"))
            ...
        """
        return edge in self.edges

    def contain_undirected_edge(self, edge: tuple[str, ...]) -> bool:
        """Verifica se um arco não-direcionado está no grafo.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices, ou seja, o arco.

        Returns:
            bool: Se o arco existe no grafo.

        Examples:
            Graph().contain_undirected_edge(("1", "2"))

            Graph().contain_undirected_edge(("A", "C"))
            ...
        """
        return edge in self.edges and tuple(reversed(edge)) in self.edges
    
    def get_edge_weight(self, edge: tuple[str, ...]) -> int:
        """Retorna o custo de um arco do grafo, caso exista.

        Args:
            edge (tuple[str, ...]): Os rótulos dos vértices, ou seja, o arco.

        Returns:
            int: O custo do arco.
        
        Examples:
            Graph().get_edge_weight(("1", "2"))

            Graph().get_edge_weight(("A", "B"))
            ...
        """
        if self.contain_directed_edge(edge):
            return self.edges[edge]
        return 0

    def get_vertexes_degree(self) -> list[int]:
        """Faz a contagem de graus, para todos os vértices, do grafo.

        Returns:
            list[int]: A contagem de graus do grafo.
        """
        return [
            self.vertex_count - self.graph[i].count(0) for i, _ in enumerate(self.graph)
        ]

    def get_vertexes_degree_sum(self) -> int:
        """Pega a quantidade máxima, a soma, dos graus, dos vértices, do grafo.

        Returns:
            int: A soma dos graus dos vértices.
        """
        return sum(self.get_vertexes_degree())

    def get_graph_density(self) -> float:
        """Pega a densidade do grafo.

        Returns:
            float: A densidade do grafo.
        """
        return self.get_vertexes_degree_sum() / self.vertex_count

    def get_graph_frequency(self) -> dict[int, int]:
        """Pega a frequência dos vértices do grafo.

        Returns:
            dict[int, int]: A frequência dos vértices do grafo.
        """
        return dict(Counter(sorted(self.get_vertexes_degree())))

    def find_vertexes_with_max_degree(self) -> list[str]:
        """Retorna todos os vértices de grau máximo no grafo.

        Returns:
            list[str]: Os rótulos dos vértices de grau máximo.
        """
        return self.find_vertexes_with_degree(max(self.get_vertexes_degree()))

    def find_vertexes_with_min_degree(self) -> list[str]:
        """Retorna todos os vértices de grau mínimo no grafo.

        Returns:
            list[str]: Os rótulos dos vértices de grau mínimo.
        """
        return self.find_vertexes_with_degree(min(self.get_vertexes_degree()))

    def find_vertexes_with_degree(self, degree: int) -> list[str]:
        """Retorna todos os vértices com determinado grau no grafo.

        Args:
            degree (int): O grau a ser procurado nos vértices do grafo.

        Returns:
            list[str]: Os rótulos dos vértices com tal grau.
        """
        graph_degree = self.get_vertexes_degree()
        return [
            self.vertexes[vertex]
            for vertex, deg in enumerate(graph_degree)
            if deg == degree
        ]

    def find_adjacent_vertexes(self, vertexes: tuple[str, ...] | str) -> dict[str, list[str]]:
        """Retorna os vértices adjacentes de um ou mais vértices.

        Args:
            vertexes (tuple[str, ...] | str): O rótulo de um ou mais vértice, de um grafo.
        
        Returns:
            dict[str, list[str]]: Os rótulos dos vértices adjacentes dos vértices fornecidos.
        """

        def add_adjacent_vertex_to_data(target_vertex: str):
            """Adiciona os vértices adjacentes nos vizinhos encontrados.

            Args:
                target_vertex (str): O rótulo do vértice atual.
            """
            for vertex in self.vertexes:
                if (target_vertex, vertex) in self.edges.keys():
                    neighbors[target_vertex].append(vertex)

        # Inicializa os dicionários, com o vértice e seus vizinhos.
        neighbors = {}
        for target_vertex in vertexes:
            neighbors[target_vertex] = []

        # Pega os vizinhos para cada vértice fornecido.
        if isinstance(vertexes, tuple):
            for target_vertex in vertexes:
                add_adjacent_vertex_to_data(target_vertex)
        if isinstance(vertexes, str):
            add_adjacent_vertex_to_data(vertexes)

        # Retorna os vizinhos.
        return neighbors
    
    def translate_vertex_index_to_label(self, vertex: int) -> str:
        """Transforma o índice de um vértice para o rótulo.

        Args:
            vertex (int): O índice do vértice a ser buscado.

        Returns:
            str: O rótulo do vértice.
        """
        if len(self.vertexes) != 0:
            if vertex <= len(self.vertexes) - 1:
                return self.vertexes[vertex]
            else:
                raise ValueError("Não existe nenhum vértice com esse índice.")
        else:
            raise ValueError("O grafo não possui nenhum vértice.")

    def translate_vertex_label_to_index(self, vertex: str) -> int:
        """Transforma o rótulo de um vértice para o índice.

        Args:
            vertex (str): O rótulo do vértice a ser buscado.

        Returns:
            int: O índice do vértice.
        """
        if self.contain_vertex(vertex):
            return self.vertexes.index(vertex)
        else:
            raise ValueError("O grafo não possui o vértice: " + vertex)
