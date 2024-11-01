from enum import Enum
from typing import (
    Any,
    Dict,
    Generator,
    List,
    Optional,
    OrderedDict,
    Self,
    Set,
    Tuple,
    TypeAlias,
)

# https://www.youtube.com/watch?v=EFg3u_E6eHU

VertexId = int


class Vertex:

    int_to_char = [
        "0",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]

    def __init__(self, id: int, repr_as_int: bool = False):
        self.id: VertexId = id
        self.status = ExplorationStatus.UNEXPLORED
        self.repr_as_int = repr_as_int

    def explore(self):
        self.status = ExplorationStatus.EXPLORED

    # Define __eq__ method to compare vertices based on id
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vertex):
            return False
        return self.id == other.id

    # Define __hash__ method based on id
    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        char = Vertex.int_to_char[self.id]
        if char is None or self.repr_as_int:
            return f"{self.id}"
        return char

    @staticmethod
    def int_to_char_dict() -> Dict[int, str]:
        return {i: Vertex.int_to_char[i] for i in range(len(Vertex.int_to_char))}


class ExplorationStatus(Enum):
    EXPLORED = 1
    UNEXPLORED = 0


EdgeWeight: TypeAlias = int


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

    def __hash__(self) -> int:
        # Combine the hash values of weight, from_v, and to_v
        return hash((self.weight, self.from_v, self.to_v))


WeightSoFar = int


Coords = Tuple[float, float, float]


class GraphMap:
    def __init__(self, empty: None = None):
        self.vertices: Dict[Coords, Vertex] = dict()
        self.edges: Set[Edge] = set()

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
    def define_edge(
        self, weigth: int, id_from: int, id_to: int, is_bidirected=False
    ) -> Optional[Edge]:
        if id_from == id_to:
            return None
        vertex_from = None
        vertex_to = None
        # Check if the vertex exists in the Graph
        for vertex in self.vertices.values():
            if vertex.id == id_from:
                vertex_from = vertex
            elif vertex.id == id_to:
                vertex_to = vertex
        if vertex_from is None or vertex_to is None:
            return None

        edge = Edge(weigth, vertex_from, vertex_to)

        self.edges.add(edge)
        if is_bidirected:
            self.edges.add(Edge(weigth, vertex_to, vertex_from))
        return edge

    def get_adjacent_to(self, src: Vertex) -> Optional[list[Tuple[Vertex, EdgeWeight]]]:

        adjacent_vertexes = list()

        # search for the edges that have the `src` vertex as the starting point
        for edge in self.edges:
            if edge.from_v.id == src.id:
                adjacent_vertexes.append((edge.to_v, edge.weight))

        if len(adjacent_vertexes) > 0:
            return adjacent_vertexes
        return None

    def get_vertexes_ids(self) -> List[Vertex]:
        return [
            vertex
            for vertex in sorted(list(self.vertices.values()), key=lambda x: x.id)
        ]

    def debug(self):
        # print vertexes
        print(f"GraphMap: {hex(id(self))}")
        print("  (xxx, yyy) - id: id")
        for coords, vertex in sorted(self.vertices.items()):
            print(f"  ({coords[0]:3}, {coords[1]:3}) - id:{vertex.id:2}")
        # Amount of vertices:
        vertices = list(self.vertices.values())
        vertices = sorted(vertices, key=lambda x: x.id)
        num_vertices = len(vertices)
        if num_vertices > 0:
            # Create an empty adjacency matrix filled with "zeros"
            matrix = [["_" for _ in range(num_vertices)] for _ in range(num_vertices)]

            # Fill the matrix with edge weights
            for edge in self.edges:
                from_idx = vertices.index(edge.from_v)
                to_idx = vertices.index(edge.to_v)
                matrix[from_idx][to_idx] = edge.weight
                print(f"weight[{from_idx}][{to_idx}] = {edge.weight}")
            print("Matriz de Adyacencia:")

            # Get the vertex IDs as labels
            vertex_ids = [vertex.__str__() for vertex in vertices]

            # Print the header (vertex IDs)
            print("    " + "  ".join(f"{vid:2}" for vid in vertex_ids))

            # Print the matrix rows with vertex ID labels
            for i in range(num_vertices):
                row_label = f"{vertex_ids[i]:2}"
                row = " ".join(
                    "{:>3}".format(str(matrix[i][j])) for j in range(num_vertices)
                )
                print(f"{row_label} {row}")


class Dijkstra:

    @staticmethod
    def new(
        graph: GraphMap,
        start_vertex: Vertex | VertexId,
        target_vertex: Vertex | VertexId,
    ) -> Optional["Dijkstra"]:
        if isinstance(start_vertex, Vertex):
            start_vertex = start_vertex.id
        if isinstance(target_vertex, int):
            target_vertex = Vertex(target_vertex)

        for vertex in graph.vertices.values():
            # Find if the starting vertex exists
            if vertex.id == start_vertex:
                start_vertex = vertex
            if vertex.id == target_vertex.id:
                target_vertex = vertex
            # Mark vertexes as unexplored
            vertex.status = ExplorationStatus.UNEXPLORED

        if isinstance(start_vertex, int):
            return None

        return Dijkstra(graph, start_vertex, target_vertex, I_KNOW_WHAT_IM_DOING=True)

    def __init__(
        self,
        graph: GraphMap,
        start_vertex: Vertex,
        target_vertex: Vertex,
        I_KNOW_WHAT_IM_DOING=False,
    ) -> None:
        if not I_KNOW_WHAT_IM_DOING:
            raise ValueError(
                "This class is not meant to be instantiated directly. Use Dijkstra.new() instead"
            )
        self.graph = graph
        self.vertex_weight: Dict[Vertex, WeightSoFar | None] = dict()
        for vertexes in self.graph.vertices.values():
            self.vertex_weight.update({vertexes: None})

        self.vertex_weight[start_vertex] = 0
        self.target_vertex = target_vertex
        self.return_vertex: Dict[Vertex, Vertex | None] = dict()
        self.solution = self._advance()
        self.steps: int = 0

    def advance(
        self, steps: int = 1, debug: bool = False
    ) -> Tuple[Vertex | None, List[Tuple[Vertex, EdgeWeight]]]:
        step_result: Tuple[Vertex | None, List[Tuple[Vertex, EdgeWeight]]] = (None, [])
        for _ in range(steps):
            self.steps += 1
            step_result = next(self.solution, (None, []))
            if step_result is None:
                return (None, [])
            if debug:
                print(f"Debug Step: {self.steps}")
                self.debug()
        return step_result

    def _advance(
        self,
    ) -> Generator[Tuple[Vertex, List[Tuple[Vertex, EdgeWeight]]], None, None]:
        self.shortest_path = None
        smallest_vertex = self.get_next_smallest()
        if smallest_vertex is None:
            raise ValueError("No smallest vertex found")
        # vertex_queue = [start_vertex]
        while True:
            if smallest_vertex is None:
                break
            # Mark as explored
            neighbour_nodes = self.get_adjacent(smallest_vertex)
            smallest_vertex.explore()
            src_vertex = smallest_vertex

            if neighbour_nodes is None:
                smallest_vertex = self.get_next_smallest()
                continue

            # neighbour, weight_to_neighbour
            for neighbour, weight_to in neighbour_nodes:
                weight_till_neighbour = self.vertex_weight[neighbour]
                this_weight = self.get_weight(src_vertex)
                if (weight_till_neighbour) is None or (
                    this_weight + weight_to < weight_till_neighbour
                ):
                    self.vertex_weight[neighbour] = this_weight + weight_to
                    self.return_vertex[neighbour] = src_vertex
                yield (
                    src_vertex,
                    neighbour_nodes,
                )
            smallest_vertex = self.get_next_smallest()
        print(f"End of the line {self.steps}")

    def get_start_vertex(self) -> Vertex:
        for v, w in self.vertex_weight.items():
            if w == 0:
                return v
        raise ValueError("No starting vertex found")

    def get_next_smallest(self) -> Vertex | None:
        # Get the next smallest vertex that isn't explored

        smallest_vertex: List[Tuple[Vertex, WeightSoFar]] = []
        for vertex, weight in self.vertex_weight.items():
            if weight is None:
                continue
            if vertex.status == ExplorationStatus.EXPLORED:
                continue
            # Skip Node Weights bigger than target's Node's Weight
            # targets_weight = self.vertex_weight[self.target_vertex]
            # if targets_weight is not None and weight > targets_weight:
            #     continue
            smallest_vertex.append((vertex, weight))
        smallest_vertex.sort(key=lambda x: x[1])
        for vertex, _weight in smallest_vertex:
            return vertex
        return None

    def get_weight(self, vertex: Vertex) -> WeightSoFar:
        """For the checked alternative, directly call the self.vertex_weight[vertex]

        Raises:
            ValueError: Raises error when the vertex has no weight

        Returns:
            WeightSoFar: the weight (int) value of this vertex
        """
        weight = self.vertex_weight[vertex]
        if weight is None:
            raise ValueError("No weight found for vertex")
        return weight

    def get_adjacent(self, vertex: Vertex) -> Optional[list[Tuple[Vertex, EdgeWeight]]]:
        # Get Adjacent Vertexes
        vertexes = self.graph.get_adjacent_to(vertex)
        if vertexes is None:
            return None
        # Filter out vertexes marked as explored
        # Vertexes are meant to be marked as explored when said vertex was used to search for adjacent vertexes
        # For example. in this function that retrieves ajacent vertexes, `vertex` should be marked as explored
        vertexes = list(
            filter(lambda x: x[0].status == ExplorationStatus.UNEXPLORED, vertexes)
        )
        if len(vertexes) == 0:
            return None
        return vertexes

    def debug(self) -> None:
        print(f"Return Paths:\n")
        print(f"Vertex: (Weight of Vertex) -> return_vertex")
        for this, to in self.return_vertex.items():
            t = "None"
            if to is not None:
                t = str(to)
            print(f"{this}({self.vertex_weight[this] :3})->{t}")

        print("\n")


def main_1():
    # https://www.youtube.com/watch?v=EFg3u_E6eHU
    map = GraphMap()
    map.register_vertexes(
        [
            (Vertex(1), (0, 0)),
            (Vertex(3), (1, 2)),
            (Vertex(6), (1, -1)),
            (Vertex(5), (2, 1)),
            (Vertex(4), (3, 3)),
            (Vertex(7), (3, -1)),
            (Vertex(2), (4, 1)),
        ]
    )
    edges = [
        (3, 1, 3),
        (2, 1, 6),
        (2, 3, 6),
        (1, 3, 5),
        (3, 6, 5),
        (5, 6, 7),
        (6, 6, 2),
        (2, 5, 2),
        (4, 3, 4),
        (1, 4, 2),
        (2, 7, 2),
    ]
    for weight, _from, to in edges:
        map.define_edge(weight, _from, to, True)

    map.debug()
    Dijkstra.new(map, 1, 2).advance(30, True)
    print("Dijkstra at main_1()")


# main_1()


def main_2() -> None:

    # Should be the map below
    # https://www.youtube.com/watch?v=EFg3u_E6eHU
    map = GraphMap()
    vertexes: list[Tuple[Vertex, Tuple[float, float, float]]] = [
        (Vertex(19), (2, 3, 0.5)),
        (Vertex(1), (0, 1, -1)),
        (Vertex(2), (2.8, 0, -1)),
        (Vertex(3), (6.8, 2.8, -1)),
        (Vertex(4), (0.0, -1, 2)),
        (Vertex(5), (6.7, -4.0, -1)),
        (Vertex(6), (1.0, -3.5, 1)),
        (Vertex(7), (4.0, -3.3, 1.5)),  # G
        (Vertex(8), (2.0, -2, -1)),  # H
        (Vertex(9), (7.0, -1, 0)),  # I
        (Vertex(10), (10.0, -1, -1)),  # J
        (Vertex(11), (8.5, -2.5, 1)),  # K
        (Vertex(12), (8.5, 0.5, 1)),  # L
    ]
    vertexes = [(v, (x * 2, y * 2, z * 2)) for v, (x, y, z) in vertexes]
    map.register_vertexes(vertexes)

    edges = [
        (3, 1, 2),
        (4, 1, 4),
        (7, 1, 19),
        (4, 2, 4),
        (1, 2, 8),
        (2, 2, 19),
        (3, 3, 19),
        (2, 3, 12),
        (4, 12, 9),
        (4, 12, 10),
        (6, 9, 10),
        (4, 9, 11),
        (4, 10, 11),
        (5, 11, 5),
        (2, 5, 7),
        (2, 7, 8),
        (3, 6, 8),
        (5, 4, 6),
    ]
    for weight, _from, to in edges:
        map.define_edge(weight, _from, to, True)

    # map.debug()
    dijkstra = Dijkstra.new(map, 19, 5)
    steps = 500  # Some arbitrary step amount
    if dijkstra is None:
        raise Exception("Map is None")
    dijkstra.advance(steps, True)


# main_2()
