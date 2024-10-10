from enum import Enum
from typing import Dict, Generator, List, Optional, Self, Set, Tuple

# https://www.youtube.com/watch?v=EFg3u_E6eHU

VertexId = int


class Vertex:

    def __init__(self, id: int):
        self.id: VertexId = id
        self.explored = ExplorationStatus.UNEXPLORED
        # if can_go_to is None:
        #     can_go_to = []
        # self.can_go_to: list[int]

    def explore(self):
        self.explored = ExplorationStatus.EXPLORED

    # Define __eq__ method to compare vertices based on id
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vertex):
            return False
        return self.id == other.id

    # Define __hash__ method based on id
    def __hash__(self) -> int:
        return hash(self.id)


class ExplorationStatus(Enum):
    EXPLORED = 1
    UNEXPLORED = 0


EdgeWeight = int


class Edge:
    def __init__(self, weight: EdgeWeight, from_v: Vertex, to_v: Vertex):
        self.weight = weight
        self.from_v: Vertex = from_v
        self.to_v: Vertex = to_v

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Edge):
            return (
                self.weight == other.weight
                and self.from_v == other.from_v
                and self.to_v == other.to_v
            )
        raise ValueError(
            f"An object of type {type(other)} was passed when an object of type {Edge} was expected"
        )

    def targets_vertex(self, other_vertex: Vertex):
        return self.to_v == other_vertex

    def __hash__(self) -> int:
        # Combine the hash values of weight, from_v, and to_v
        return hash((self.weight, self.from_v, self.to_v))


WeightSoFar = int


# class GraphVertex:
#     def __init__(
#         self,
#         vertex: Vertex,
#         weight_from_origin: WeightSoFar | None = None,
#         return_vertex: Vertex | None = None,
#     ):
#         self.vertex = vertex
#         self.weight_from_origin = weight_from_origin
#         self.return_vertex = return_vertex

#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, Vertex):
#             return self.vertex == other
#         if not isinstance(other, GraphVertex):
#             return False

#         return self.vertex == other.vertex

#     def __hash__(self) -> int:
#         return hash(self.vertex)

#     def set_return(self, vertex: Vertex, new_weight: int):
#         if vertex is not Vertex:
#             raise ValueError(
#                 f"A value of type {type(vertex)} was passed when a value of type {Vertex} was expected"
#             )
#         self.return_vertex = vertex


Coords = Tuple[float, float]


class GraphMap:

    vertices: Dict[Coords, Vertex] = dict()
    edges: Set[Edge] = set()

    # Adds a vertex to the graph
    def register_vertexes(
        self, vertices: list[Tuple[Vertex, Coords]] | Tuple[Vertex, Coords]
    ):
        if isinstance(vertices, tuple):  # UnFlatten the tuple
            vertices = [vertices]

        for node in vertices:
            self.vertices.update({node[1]: node[0]})
        return

    # Adds an edge to the graph. Returns early when the vertex's id is missing
    def define_edge(self, weigth: int, id_from: int, id_to: int) -> Optional[Edge]:
        if id_from == id_to:
            return None
        vertex_from = None
        vertex_to = None
        for vertex in self.vertices.values():
            if vertex.id == id_from:
                vertex_from = vertex
            elif vertex.id == id_to:
                vertex_to = vertex

        if vertex_from is None:
            return None
        if vertex_to is None:
            return None

        edge = Edge(weigth, vertex_from, vertex_to)

        self.edges.add(edge)
        return edge

    def get_adjacent_vertexes(
        self, src: Vertex | VertexId
    ) -> Optional[list[Tuple[Vertex, EdgeWeight]]]:
        if isinstance(src, Vertex):
            src = src.id

        adjacent_vertexes = list()

        for edge in self.edges:
            if edge.from_v.id == src:
                adjacent_vertexes.append((edge.to_v, 0))
        if len(adjacent_vertexes) > 0:
            return adjacent_vertexes
        return None


class Dijkstra:
    vertexes_weight: Dict[Vertex, WeightSoFar | None]
    steps: int = 0
    solution: Generator[Optional[Tuple]]

    @staticmethod
    def new(graph: GraphMap, start_vertex: Vertex | VertexId) -> Optional["Dijkstra"]:
        if isinstance(start_vertex, Vertex):
            start_vertex = start_vertex.id

        for vertex in graph.vertices.values():
            # Find if the starting vertex exists
            if vertex.id == start_vertex:
                start_vertex = vertex
            # Mark vertexes as unexplored
            vertex.explored = ExplorationStatus.UNEXPLORED

        if isinstance(start_vertex, int):
            return None
        return Dijkstra(graph, start_vertex)

    def __init__(self, graph: GraphMap, start_vertex: Vertex) -> None:
        self.graph = graph
        for vertexes in self.graph.vertices.values():
            self.vertexes_weight.update({vertexes: None})

        self.vertexes_weight[start_vertex] = 0
        self.solution = self.gen_solution()

    def advance(self, steps: int = 1):
        for _step in range(steps):
            self.steps += 1
            next(self.solution, None)

    def gen_solution(self) -> Generator[Tuple[()]]:
        self.shortest_path = None
        start_vertex = None
        for vertex, weight_so_far in self.vertexes_weight.items():
            if weight_so_far == 0:
                start_vertex = vertex
                break
        else:
            raise ValueError("No starting vertex found")
        adjacent_vertexes = self.graph.get_adjacent_vertexes(start_vertex)
        
        while self.shortest_path == None:

            yield ()
