from typing import Any, Callable, OrderedDict, Set, Tuple
from manim import *
from manim.typing import Point3D

from vertex import Dijkstra, Edge, GraphMap, Vertex


def unique_edges(edges: Set[Edge]) -> Set[Edge]:
    """Definition of an Unique Edge:
    We assume edges are bidirectional; so it means `Vertex(1) -> Vertex(2)` is the same as `Vertex(2) -> Vertex(1)`
    Also assumes that the weight is the same for both edges.

    # The implementation detail
    compare the index, sorting the id in ascending order.
    This means that for an edge as `Vertex(2) -> Vertex(1)` will be converted to `Vertex(1) -> Vertex(2)` and
    then compared with the seen edges
    """
    seen = set()
    for edge in edges:
        if edge.from_v.id > edge.to_v.id:
            edge = Edge(edge.weight, edge.to_v, edge.from_v)
        if edge in seen:
            continue
        seen.add(edge)
    return seen


class Manim_Dijkstra(Scene):  # type: ignore
    def __init__(self, random: Any = 0):
        super().__init__()
        dijkstra, steps = dijkstra_func_1()
        self.dijkstra: Dijkstra = dijkstra
        self.steps: int = steps
        # Holds the Mobjects of the vertexes and their weights
        # TODO Consider giving it a more fitting name. This has been working as a sort of Stack flow
        self.vertex_weights: Dict[Vertex, Tuple[MathTex, int | None, Arrow | None]] = (
            dict()
        )
        self.highlight_rectangle = Rectangle(TEAL_D, 1.5, 1.5).set_z_index(1)
        self.g: Graph

        # self.weights_labels: dict[Tuple[Vertex, Vertex], Tuple[Tex, Rectangle]] = dict()
        # TODO Undo debug settings
        config.frame_rate = 60
        self.animate_drawing_weighted_edges = True  # Default: True
        self.animate_drawing_node_weights = self.animate_drawing_weighted_edges

    def draw_weigthed_edges(self) -> None:
        # Weights Setup: Get the midpoint between vertexes
        positions: OrderedDict[Tuple[Vertex, Vertex], Point3D] = OrderedDict()
        for from_v, to_v in [
            (edge.from_v, edge.to_v) for edge in unique_edges(self.dijkstra.graph.edges)
        ]:
            pos1 = self.dijkstra.graph.get_vertex_position(from_v)
            pos2 = self.dijkstra.graph.get_vertex_position(to_v)
            pos = ((pos1[0] + pos2[0]) / 2, (pos1[1] + pos2[1]) / 2, 0.0)
            # Sort the vertex index
            if from_v.id > to_v.id:
                from_v, to_v = to_v, from_v
                raise ValueError(
                    "UNREACHABLE CODE : The vertexes should've been sorted due to call of `unique_edges() which return edges in ascending order`"
                )
            positions.update({(from_v, to_v): pos})

        # Instantiate Animations
        animations: list[Tuple[Tex, Rectangle]] = list()
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
            tex_weight = Tex(str(weight)).move_to(pos).set_color(TEAL_E)
            weight_background.set_z_index(1)
            tex_weight.set_z_index(2)
            animations.append((tex_weight, weight_background))

        # Commit the Animations
        if self.animate_drawing_weighted_edges:
            rects = [FadeIn(rect) for rect, _ in animations]
            anims = [Write(anim) for _, anim in animations]
            self.play(
                AnimationGroup(
                    LaggedStart(anims, lag_ratio=0.4),
                    LaggedStart(rects, lag_ratio=0.3),
                    lag_ratio=0.4,
                    run_time=4,
                    rate=rate_functions.ease_in_cubic,
                ),
            )
            [anim.animate.set_z_index(10) for _, anim in animations]
            del animations
        else:
            # Flatten the tuple
            animations = [
                anim for anims in animations for anim in anims
            ]  # If you praise me, or judge me for this: Copilot suggested this.
            self.add(*animations)

    def draw_node_weight(self) -> None:
        # retrieve vertexes in ascending order
        vertexes = self.dijkstra.graph.get_vertexes_ids()
        self.vertex_weights: Dict[Vertex, Tuple[MathTex, int | None, Arrow | None]] = (
            dict()
        )
        for v in vertexes:
            node_weight = self.dijkstra.vertex_weight[v]

            if node_weight is None:
                weight_label = MathTex("\infty")
            else:
                weight_label = MathTex(str(node_weight))
            weight_label.next_to(self.g.vertices[v], DOWN).set_color(PURPLE_A)
            self.vertex_weights[v] = (weight_label, node_weight, None)
        if self.animate_drawing_node_weights:
            anims = [Write(tex) for tex, *_ in self.vertex_weights.values()]
            self.play(LaggedStart(*anims, lag_ratio=0.4), run_time=2.5)
        else:
            anims = [tex for tex, *_ in self.vertex_weights.values()]
            self.add(*anims)

    def construct(self):
        # region: SETUP graph
        vertices = self.dijkstra.graph.get_vertexes_ids()
        unique_edges = self.get_unique_edges_vertexes()
        vertices_layout = self.dijkstra.graph.get_vertexes_layout()

        edge_config = {
            "stroke_width": 2,
            (
                Vertex(3),
                Vertex(1),
            ): {  # Vestige code so I can use this as an example in the future
                "stroke_width": 10.0,
                "color": BLUE,
                "tip_config": {"tip_length": 0.25, "tip_width": 0.25},
            },
        }

        self.g = g = Graph(
            vertices,
            unique_edges,
            labels=True,
            layout=vertices_layout,
            edge_config=edge_config,
        ).scale(1)
        self.highlight_rectangle.move_to(
            g.vertices[self.dijkstra.get_start_vertex()].get_center()
        )
        self.camera.frame_center = g.get_center()
        self.camera.frame_width = self.camera.frame_width * 1.2
        self.camera.frame_height = self.camera.frame_height * 1.2
        self.play(Write(g))
        self.draw_weigthed_edges()
        self.draw_node_weight()
        self.wait()
        # endregion: SETUP

        self.play(
            Write(
                Text("Dijkstra's Algorithm")
                .scale(0.8)
                .next_to(self.g, UP)
                .set_color_by_gradient(
                    AS2700.G23_SHAMROCK, AS2700.G36_KIKUYU, AS2700.T14_MALACHITE
                )
            )
        )

        start_vertex = self.dijkstra.get_start_vertex()
        label = self.vertex_weights[start_vertex][0]
        self.play(
            Write(
                self.highlight_rectangle.move_to(
                    (self.g.vertices[start_vertex].get_center() + label.get_center())
                    / 2
                )
            )
        )

        failsafe = 30
        # context = Text("").set_color(RED).next_to(g, DOWN) # Commented out because I'm no longer debugging
        while failsafe:
            failsafe -= 1
            root_vertex = self.dijkstra.advance(1, True)
            if root_vertex is None:
                break

            for this, ret_to in self.dijkstra.return_vertex.items():
                if ret_to is None:
                    continue
                new_weight = self.dijkstra.vertex_weight[this]
                if new_weight is None:
                    raise Exception("Unexpected case : Vertex weight is None")
                current_tex, weight, arrow = self.vertex_weights[this]

                if weight == new_weight:
                    continue
                # Update the data linked to `this` vertex
                new_arrow = self.arrow_at(this, ret_to)
                self.vertex_weights[this] = (current_tex, new_weight, new_arrow)

                new_weight = (
                    MathTex(str(new_weight))
                    .set_color(current_tex.get_color())
                    .move_to(current_tex.get_center())
                )

                moving_dot = Dot(
                    g.vertices[root_vertex].get_center(),
                    color=LIGHT_PINK,
                    radius=0.2,
                    fill_opacity=1,
                )

                self.play(
                    self.highlight_rectangle.animate.move_to(
                        (new_weight.get_center() + self.g.vertices[this].get_center())
                        / 2
                    ),
                    run_time=1,
                )
                if arrow is None:
                    arrow_animation = Write(new_arrow)
                else:
                    arrow_animation = ReplacementTransform(arrow, new_arrow)
                self.play(
                    LaggedStart(
                        moving_dot.animate.move_to(g.vertices[this].get_center()),
                        arrow_animation,
                        Transform(current_tex, new_weight),
                        lag_ratio=0.6,
                    ),
                    run_time=1.5,
                )
                current_tex.become(new_weight)
                self.play(FadeOut(moving_dot), run_time=0.5)
        # And playout the final scene of going from start to end
        # Draw out the path needed
        path = self.get_path_resolution_animation()
        self.play(
            LaggedStart(FadeOut(self.highlight_rectangle), *path, lag_ratio=0.6),
            run_time=4,
        )
        self.wait()

    def get_path_resolution_animation(self) -> List[ReplacementTransform]:
        goal = self.dijkstra.target_vertex
        if goal is None:
            raise Exception("Unexpected case : Target vertex is None")
        anims = []
        while True:
            return_vertex = self.dijkstra.return_vertex.get(goal)
            if return_vertex is None:
                break
            _mathtex, val, old_arrow = self.vertex_weights[goal]
            new_arrow = self.arrow_at(return_vertex, goal, False).set_color(
                AS2700.B23_BRIGHT_BLUE
            )
            anims.append(ReplacementTransform(old_arrow, new_arrow))
            self.vertex_weights[goal] = (
                _mathtex,
                val,
                new_arrow,
            )  # Update the object to properly reflec the scene's state
            goal = return_vertex
        anims.reverse()
        return anims

    def arrow_at(self, from_v: Vertex, to_v: Vertex, short: bool = True) -> Arrow:
        start = self.dijkstra.graph.get_vertexes_layout()[from_v]
        end = self.dijkstra.graph.get_vertexes_layout()[to_v]
        if short:
            end = np.array(end) + (np.array(start) - np.array(end)) * 0.65
        else:
            end = np.array(end)
        return Arrow(start, end, color=RED_E, max_tip_length_to_length_ratio=0.8)

    def get_unique_edges(self) -> Set[Edge]:
        return unique_edges(self.dijkstra.graph.edges)

    def get_unique_edges_vertexes(self) -> Set[Tuple[Vertex, Vertex]]:
        return set([(edge.from_v, edge.to_v) for edge in self.get_unique_edges()])


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
