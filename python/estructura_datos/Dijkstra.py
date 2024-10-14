from typing import Any, Callable, OrderedDict, Tuple
from manim import *
from manim.typing import Point3D


from vertex import Dijkstra, GraphMap, Vertex


class Manim_Dijkstra(Scene):  # type: ignore
    def __init__(self, random: Any = 0):
        super().__init__()
        dijkstra, steps = dijkstra_func_1()
        self.dijkstra: Dijkstra = dijkstra
        self.steps: int = steps
        # TODO Undo debug settings
        config.frame_rate = 24
        self.animate_drawing_weighted_edges = False  # Default: True

    def draw_weigthed_edges(self) -> Any:
        # Weights Setup: Get the midpoint between vertexes
        positions: OrderedDict[Tuple[Vertex, Vertex], Point3D] = OrderedDict()
        for from_v, to_v in self.dijkstra.graph.get_edges():
            pos1 = self.dijkstra.graph.get_vertex_position(from_v)
            pos2 = self.dijkstra.graph.get_vertex_position(to_v)
            pos = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2, 0.0)
            # Sort the vertex index
            if from_v.id > to_v.id:
                from_v, to_v = to_v, from_v
            positions.update({(from_v, to_v): pos})

        # Instantiate Animations
        animations: list[Tuple[Rectangle, Tex]] = list()
        for (from_v, to_v), pos in positions.items():
            # find the matching edge in the graph
            for edge in self.dijkstra.graph.edges:
                if edge.from_v == from_v and edge.to_v == to_v:
                    weight = edge.weight
                    break
            else:
                raise Exception("Unexpected case : Edge not found")
            weight_background = (
                Rectangle(width=0.5, height=0.5, fill_color=BLACK, fill_opacity=1)
                .move_to(pos)
                .set_stroke(GREEN_A, opacity=0.7)
            )
            weight = Tex(str(weight)).move_to(pos).set_color(TEAL_E)
            animations.append((weight_background, weight))

        # Commit the Animations
        if self.animate_drawing_weighted_edges:
            animations = [
                AnimationGroup(FadeIn(rect), Create(anim))
                for (rect, anim) in animations
            ]
            self.play(LaggedStart(*animations, lag_ratio=0.3), run_time=3)
            del animations
        else:
            # Flatten the tuple
            animations = [
                anim for anims in animations for anim in anims
            ]  # If you praise me, or judge me for this: Copilot suggested this.
            self.add(*animations)

    def construct(self):
        vertices = self.dijkstra.graph.get_vertexes_ids()
        edges = [(to_v, from_v) for from_v, to_v in self.dijkstra.graph.get_edges()]
        vertices_layout = self.dijkstra.graph.get_vertexes_layout()

        edge_config = {
            "stroke_width": 2,
            "tip_config": {
                "tip_shape": StealthTip,
                "tip_length": 0.15,
            },
            (Vertex(1), Vertex(3)): {
                "color": BLUE_E,
            },
        }

        g = Graph(
            vertices,
            edges,
            labels=True,
            layout=vertices_layout,
            edge_config=edge_config,
        ).scale(1)
        
        self.camera.frame_center = g.get_center()
        self.play(Create(g))
        self.draw_weigthed_edges()
        self.wait()


def dijkstra_func_1() -> Tuple[Dijkstra, int]:
    # Should be the map below
    # https://www.youtube.com/watch?v=EFg3u_E6eHU
    map = GraphMap()
    vertexes: list[Tuple[Vertex, Tuple[float, float]]] = [
        (Vertex(1), (0, 0)),
        (Vertex(3), (1, 1.5)),
        (Vertex(6), (1, -1)),
        (Vertex(5), (2, 0)),
        (Vertex(4), (3, 1.5)),
        (Vertex(7), (3, -1.2)),
        (Vertex(2), (4, 0)),
    ]
    vertexes = [(v, (x * 2, y * 2)) for v, (x, y) in vertexes]
    map.register_vertexes(vertexes)

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

    # map.debug()
    dijkstra = Dijkstra.new(map, 1, 2)
    steps = 30  # Some arbitrary step amount
    if dijkstra is None:
        raise Exception("Map is None")

    return (dijkstra, steps)


Manim_Dijkstra().render(True)
