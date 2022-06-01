# **Grafos**
### Aplicação, desenvolvida em [***Python 3.10.4***](https://www.python.org/downloads/release/python-3104/), com o principal foco na utilização e, também, manipulação de [**Grafos**](https://pt.wikipedia.org/wiki/Teoria_dos_grafos).

## **Índice**
- [**Instalação**](#1-instalação)
- [**Tipos de Grafos suportados**](#2-tipos-de-grafos-suportados)
- [**Implementações feitas**](#3-implementações-feitas)
    - [*Na classe "**Graph**"*](#1-na-classe-"graph")
    - [*Na classe "**Hamiltonian**"*](#2-na-classe-"hamiltonian")
    - [*Na classe "**Euler**"*](#3-na-classe-"euler")
    - [*Na classe "**BreadthFirstSearch**"*](#4-na-classe-"breadthfirstsearch")
    - [*Na classe "**DepthFirstSearch**"*](#5-na-classe-"depthfirstsearch")
    - [*Na classe "**ShortestMinimumPath**"*](#6-na-classe-"shortestminimumpath")
- [**Modelos de arquivos de entrada**](#4-modelos-de-arquivos-de-entrada-json)
- [**Criando grafos**](#5-criando-grafos)
- [**Aplicando Teoremas em grafos**](#6-aplicando-teoremas-em-grafos)
- [**Fazendo Buscas em grafos**](#7-fazendos-buscas-em-grafos)
- [**Gerando Árvores**](#8-plantando-árvores)
- [**Otimizando Rotas**](#9-otimizando-rotas)
- [**Licença**](#10-licença)

## 1) **Instalação**
Não tem nada *muito complexo*, basta **baixar** os arquivos e usá-lo.

## 2) **Tipos de Grafos suportados**
*Você pode criar-los utilizando a classe "Graph.py"*
1) [Grafos Simples](https://pt.wikipedia.org/wiki/Grafo_simples).
2) [Grafos Orientados](https://pt.wikipedia.org/wiki/Grafo_orientado)
3) [Grafos Completos](https://pt.wikipedia.org/wiki/Grafo_completo).
4) [Grafos Nulos](https://pt.wikipedia.org/wiki/Grafo_nulo)
5) [Grafos Regulares](https://pt.wikipedia.org/wiki/Grafo_regular)
6) [Multigrafos](https://pt.wikipedia.org/wiki/Multigrafo)

## 3) **Implementações feitas**
#### 1. *Na classe "**[Graph](Graph.py)**"*
- [Matriz de adjacência](https://pt.wikipedia.org/wiki/Matriz_de_adjac%C3%AAncia)
- [Grau/Valência de vértices](https://pt.wikipedia.org/wiki/Grau_(teoria_dos_grafos))
- Busca de vértices
- Busca de arestas
- Densidade do grafo
- Frequência do grafo
- Adição e/ou Remoção de vértices
- Adição e/ou Remoção de arestas
- Peso de uma aresta
- Verificação de existência de arestas e vértices
- Tradução de rótulo para índice e vice-versa
- Busca por adjacentes de determinado vértice
- Busca por vértices de grau máximo e mínimo
- Busca por vértices de determinado grau
- Criação de grafos a partir da leitura de arquivos [**JSON**](https://pt.wikipedia.org/wiki/JSON)
#### 2. *Na classe "**[Hamiltonian](Hamiltonian.py)**"*
- Fecho Hamiltoniano
- Teorema de Dirac
- Teorema de Ore
- Teorema de Bondy Chvatal
#### 3. *Na classe "**[Euler](Euler.py)**"*
- Verificação de grafos Eulerianos
- Verificação de grafos Semi-Eulerianos
- [Circuito Euleriano](https://pt.wikipedia.org/wiki/Caminho_euleriano)
#### 4. *Na classe "**[BreadthFirstSearch](BreadthFirstSearch.py)**"*
- [Busca em Largura (BFS)](https://pt.wikipedia.org/wiki/Busca_em_largura)
- Nível dos vértices (BFS)
- [Árvore Geradora (BFS)](https://pt.wikipedia.org/wiki/%C3%81rvore_de_extens%C3%A3o_m%C3%ADnima)
#### 5. *Na classe "**[DepthFirstSearch](DepthFirstSearch.py)**"*
- [Busca em Profundidade (DFS)](https://pt.wikipedia.org/wiki/Busca_em_profundidade)
- Nível de profundidade dos vértices (DFS)
- [Árvore de Profundidade (DFS)](https://pt.wikipedia.org/wiki/%C3%81rvore_bin%C3%A1ria)
#### 6. *Na classe "**[ShortestMinimumPath](ShortestMinimumPath.py)**"*
- [Algoritmo de Dijkstra](https://pt.wikipedia.org/wiki/Algoritmo_de_Dijkstra)
- [Algoritmo de Bellman-Ford](https://pt.wikipedia.org/wiki/Algoritmo_de_Bellman-Ford)

## 4) **Modelos de arquivos de entrada (*JSON*)**

Segue, abaixo um simples modelo de um grafo 3-regular, com 4 (quatro) vértices.

```json
{
    "Vertexes": [
        ["A", "B", "C", "D"]
    ],
    "Edges": [
        ["A", "B"], ["A", "C"], ["A", "D"],
        ["B", "A"], ["B", "C"], ["B", "D"],
        ["C", "A"], ["C", "B"], ["C", "D"],
        ["D", "A"], ["D", "B"], ["D", "A"]
    ]
}
```
É bem simples na verdade, na chave "***Vertexes***" você insere os
vértices, os seus rótulos, que o grafo possui e na chave "***Edges***",
você coloca os arcos que o grafo contem, por exemplo: ***["A", "B"]***, 
indica um arco, saindo de "***A***" e indo até "***B***" com peso **1**,
**pois nenhum peso foi fornecido** (em casos como esse, o valor **1** é
atribuído por padrão), para definir arcos com **pesos**, basta 
inserir um novo elemento, o qual indicará o peso do arco, ou seja: 
***["A", "B", 3]***, que, por fim, criaria um arco, saindo de "***A***"
e indo até "***B***", com um peso de ***3***.

## 5) **Criando grafos**

Caso preferir, você pode criar, também, grafos utilizando os próprios métodos da classe "***Graph***".

Criaremos, novamente, um grafo 3-regular de 4 (quatro) vértices, por exemplo:
```py
# Inicializamos a classe Graph.
graph = Graph()

# Adicionamos os 4 (quatro) vértices "A", "B", "C" e "D".
graph.add_vertexes(("A", "B", "C", "D"))

# Adicionamos os arcos.
graph.add_edge_undirected(("A", "B")) # A <--> B
graph.add_edge_undirected(("A", "C")) # A <--> C
graph.add_edge_undirected(("A", "D")) # A <--> D
graph.add_edge_undirected(("B", "C")) # B <--> C
graph.add_edge_undirected(("B", "D")) # B <--> D
graph.add_edge_undirected(("C", "D")) # C <--> D

# Caso queira adicionar peso aos arcos, basta passar um segundo 
# parâmetro na função "add_edge_undirected", o qual representaria o peso.
# Ex:. graph.add_edge_undirected(("A", "C"), 3)
```
*E pronto! você criou um grafo.*

## 6) **Aplicando Teoremas em grafos**

-"*Legal, temos um grafo, mas como faço para aplicar teoremas nele?*"

```py
# Com o grafo montado, basta incializar a classe desejada, passando
# o grafo criado como parâmetro durante sua inicialização.
graph = Graph()
# ... criação do grafo.

# "Hamiltonian" para teoremas hamiltonianos.
# "Euler" para teoremas eulerianos.
hamiltonian = Hamiltonian(graph)
euler = Euler(graph)

# Para aplicar o Teorema de Dirac:
hamiltonian.is_graph_dirac()

# Para aplicar o Teorema de Ore:
hamiltonian.is_graph_ore()

# Para aplicar o Teoream de Bondy Chvatal:
hamiltonian.is_graph_bondy()

# Para aplicar o Teorema Euleriano:
euler.is_graph_euler()

# Para aplicar o Teorema Semi-Euleriano.
euler.is_graph_semi_euler()
```
*Pronto! você aplicous os teoremas no grafo.*

## 7) **Fazendos Buscas em grafos**

Seguindo a mesma lógica, para aplicar as buscas em um grafo basta:

```py
# Com o grafo montado, basta inicializar a classe desejada, passando
# o grafo criado como parâmetro durante sua inicialização.
graph = Graph()
# ... criação do grafo.

# Inicializamos o "BFS", para as buscas em largura.
bfs = BreadthFirstSearch(graph)

# Para realizar a Busca em Largura, você deve definir um ponto de 
# partida, pode ser um vértice qualquer do grafo. 
bfs.apply_bfs("A")

# Inicializamos o "DFS, para as buscas em profundidade.
dfs = DepthFirstSearch(graph)

# A ideia para a Busca em Profundidade é as mesma da BFS, basta
# chamar o método e passar um ponto de partida.
dfs.apply_dfs("A")
```
*Pronto! você fez buscas em um grafo.*

## 8) **Gerando árvores**

"*Depois de brincar com as buscas em largura/profundidade, você
resolve montar suas árvores.*"

```py
# Com o grafo montado e as classes inicializadas (DFS ou BFS).
graph = Graph() 
# ...
bfs = BreadthFirstSearch(graph)
# ...
dfs = DepthFirstSearch(graph)
# ...

# Em ambas as funções, para geração de árvore, um ponto de partida
# deve ser passado como parâmetro, pois o própria método irá aplicar
# a busca no grafo fornecido e, a partir daí, gerará á Árvore.

# Basta chamar seus métodos e passar, também, um ponto de partida.
bfs.get_bfs_tree("A") # Retorna um objeto "Graph", representando a Árvore.

# Para a Árvore do DFS.
dfs.get_dfs_tree("A") # Retorna um objeto "Graph", representando a Árvore.
```
*Pronto! você gerou grafos em árvores a partir de uma busca.*

## 9) **Otimizando Rotas**

Sim, você pode obter rotas de custo mínimo, tanto para custos 
não-negativos como, também, para custos negativos e positivos.

```py
# Com o grafo montado, basta inicializar a classe, passando o grafo como parâmetro.
graph = Graph()
# ... criação do grafo.

# Inicializamos a classe responsável pelos algoritmos de caminho mínimo.
smp = ShortestMinimumPath(graph)

# Em ambos os métodos, você deve fornecer, é claro, um ponto de partida.

# Aqui você pode escolher qual algoritmo usar:
# 1) Algoritmo de Dijkstra.
smp.apply_dijkstra_algorithm("A")

# 2) Algoritmo de Bellman-Ford.
smp.apply_bellman_ford_algorithm("A")

# 3) Algoritmo de Floyd-Warshall.
smp.apply_floyd_warshall_algorithm()

# O retorno dos métodos é, basicamente, o caminho percorrido e o custo
# de cada arco percorrido.
```

## 10) **Licença**
Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE) para mais detalhes.