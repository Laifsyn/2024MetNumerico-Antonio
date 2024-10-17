from typing import Any, Callable, Optional, OrderedDict, Set, Tuple
from manim import *
from manim.typing import Point3D

from vertex import Dijkstra, Edge, EdgeWeight, GraphMap, Vertex


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


class Manim_Dijkstra(ThreeDScene):  # type: ignore
    def __init__(self, random: Any = 0):
        super().__init__()
        dijkstra, steps = dijkstra_func_2()
        self.dijkstra: Dijkstra = dijkstra
        self.steps: int = steps
        # Holds the Mobjects of the vertexes and their weights
        # TODO Consider giving it a more fitting name. This has been used as a sort of Data registry
        self.vertex_weights: Dict[Vertex, Tuple[MathTex, int | None, Arrow | None]] = (
            dict()
        )
        self.highlight_rectangle = Rectangle(TEAL_D, 1.5, 1.5).set_z_index(1)
        self.g: Graph

        # TODO Undo debug settings
        config.frame_rate = 60
        self.animate_drawing_weighted_edges = True  # Default: True
        self.animate_drawing_node_weights = self.animate_drawing_weighted_edges
        self.animate_path_resolution = self.animate_drawing_weighted_edges

    def draw_weigthed_edges(self) -> None:
        # Weight's Setup: Get the midpoint between vertexes
        positions: OrderedDict[Tuple[Vertex, Vertex], Point3D] = OrderedDict()
        for from_v, to_v in [
            (edge.from_v, edge.to_v) for edge in unique_edges(self.dijkstra.graph.edges)
        ]:
            pos1 = self.g.vertices[from_v].get_center()
            pos2 = self.g.vertices[to_v].get_center()
            pos = (pos1 + pos2) / 2
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
                    rate=rate_functions.not_quite_there,
                ),
                run_time=2.5,
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
            self.play(LaggedStart(*anims, lag_ratio=0.4), run_time=3.5)
        else:
            anims = [tex for tex, *_ in self.vertex_weights.values()]
            self.add(*anims)

    def construct(self):
        # region: SETUP graph
        vertices = self.dijkstra.graph.get_vertexes_ids()
        unique_edges = self.get_unique_edges_vertexes()
        vertices_layout = dict()
        for coords, vertex in self.dijkstra.graph.vertices.items():
            vertices_layout.update({vertex: (coords[0], coords[1], coords[2])})

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

        self.g = g = (
            Graph(
                vertices,
                unique_edges,
                labels=True,
                layout=vertices_layout,
                edge_config=edge_config,
            )
            .move_to(ORIGIN)
            .scale(1)
        )
        self.highlight_rectangle.move_to(
            g.vertices[self.dijkstra.get_start_vertex()].get_center()
        )

        # Set Camera settings
        self.camera.frame_width = g.width * 1.3
        self.camera.frame_height = self.camera.frame_width / config.aspect_ratio
        if self.camera.frame_height < g.height * 1.3:
            self.camera.frame_height = g.height * 1.3
            self.camera.frame_width = self.camera.frame_height * config.aspect_ratio
        self.camera.frame_center = g.get_center()

        self.play(Write(g), run_time=4)
        self.draw_weigthed_edges()
        self.wait(0.5)
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

        self.draw_node_weight()

        start_vertex = self.dijkstra.get_start_vertex()
        label = self.vertex_weights[start_vertex][0]
        self.play(
            Write(
                self.highlight_rectangle.move_to(self.node_label_center(start_vertex))
            )
        )

        failsafe = self.steps
        failsafe = 16
        next_vertex = self.dijkstra.get_start_vertex()
        cleanup = None
        cleanup_rects: List[Rectangle] = []

        while failsafe > 0:
            # Deactivate Highlight
            activated_highlighter = self.highlight_rectangle.copy()
            self.highlight_rectangle.become(
                self.highlight_rectangle.set_stroke(
                    GRAY_B, self.highlight_rectangle.get_stroke_width(), opacity=0.5
                )
            )
            if next_vertex is None:
                break
            adjacent_vertexes = self.dijkstra.get_adjacent(next_vertex)
            if adjacent_vertexes is None:
                adjacent_vertexes = []
            adj_len = len(adjacent_vertexes)
            root, adjacent_vertexes = self.dijkstra.advance(
                adj_len if adj_len else 1, False
            )
            failsafe -= 1
            cleanup, root, rect = self.mark_adjacent_vertexes(
                root if root is not None else next_vertex, adjacent_vertexes
            )
            cleanup_rects.append(rect)

            next_vertex = self.dijkstra.get_next_smallest()

            for adj_vertex in [adj for adj, _weight in adjacent_vertexes]:
                if root is None:
                    raise Exception("Unexpected case : Unreachable Code")
                    continue

                new_weight = self.dijkstra.vertex_weight[adj_vertex]
                if new_weight is None:
                    raise Exception("Unexpected case : Vertex weight is None")
                current_tex, weight, arrow = self.vertex_weights[adj_vertex]

                # If the weight is different to the one stored, update the weight and Arrow
                if weight is not new_weight:
                    # Update the data linked to `this` vertex
                    new_arrow = self.arrow_at(adj_vertex, root)
                    self.vertex_weights[adj_vertex] = (
                        current_tex,
                        new_weight,
                        new_arrow,
                    )
                    if arrow is None:
                        arrow_animation = Write(new_arrow.set_color(MAROON_D))
                    else:
                        arrow_animation = ReplacementTransform(arrow, new_arrow)
                else:
                    arrow_animation = Wait(run_time=0)

                weight_label = (
                    MathTex(str(new_weight))
                    .set_color(current_tex.get_color())
                    .move_to(current_tex.get_center())
                )

                moving_dot = Dot(
                    g.vertices[root].get_center(),
                    color=LIGHT_PINK,
                    radius=0.2,
                    fill_opacity=1,
                )
                activated_highlighter.move_to(self.node_label_center(adj_vertex))
                if self.animate_path_resolution:
                    self.play(
                        self.highlight_rectangle.animate.become(activated_highlighter),
                        run_time=0.7,
                    )
                    self.play(
                        LaggedStart(
                            moving_dot.animate.move_to(
                                g.vertices[adj_vertex].get_center()
                            ),
                            arrow_animation,
                            Transform(current_tex, weight_label),
                            lag_ratio=0.6,
                            run_time=1.2,
                        ),
                    )
                    current_tex.become(weight_label)
                    self.play(FadeOut(moving_dot), run_time=0.5)
                else:
                    current_tex.become(weight_label)
                    moving_dot.move_to(g.vertices[adj_vertex].get_center())
                    (
                        self.add(arrow_animation.mobject)
                        if arrow is None
                        else arrow.become(new_arrow)
                    )
                    del new_arrow
                    self.add(
                        self.highlight_rectangle.move_to(
                            self.node_label_center(adj_vertex)
                        )
                    )
            cleanup()

        # And playout the final scene of going from start to end
        # Draw out the path needed
        path = self.get_path_resolution_animation()
        self.play(
            LaggedStart(
                FadeOut(self.highlight_rectangle),
                [FadeOut(rect) for rect in reversed(cleanup_rects)],
                lag_ratio=0.3,
            ),
            run_time=2,
        )
        self.play(
            LaggedStart(
                *path,
                lag_ratio=0.6,
            ),
            run_time=4,
        )

        self.wait(1)
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, run_time=3)
        # self.wait(0.5)
        # self.move_camera(phi=105 * DEGREES, theta=15 * DEGREES, run_time=3)
        # self.wait(0.5)
        self.move_camera(phi=165 * DEGREES, theta=60 * DEGREES, run_time=3)
        self.wait(0.5)
        # self.move_camera(phi=210 * DEGREES, theta=135 * DEGREES, run_time=2)
        # self.wait(0.5)
        # self.move_camera(phi=235 * DEGREES, theta=220 * DEGREES, run_time=3)
        # self.wait(0.5)
        # self.move_camera(phi=295 * DEGREES, theta=335 * DEGREES, run_time=3)
        # self.wait(0.5)

        self.move_camera(
            phi=360 * DEGREES,
            theta=270 * DEGREES,
            run_time=2,
            rate=rate_functions.wiggle,
        )
        self.wait(2)

    def node_label_center(self, v: Vertex) -> Point3D:
        label = self.vertex_weights[v][0]
        return (self.g.vertices[v].get_center() + label.get_center()) / 2

    # Returns a CleanUp Lambda function to undo relevant animations
    def mark_adjacent_vertexes(
        self, src: Vertex, adjacents_with_weight: List[Tuple[Vertex, EdgeWeight]]
    ) -> Tuple[Callable, Vertex, Rectangle]:
        src_vertex: LabeledDot | Mobject = self.g.vertices[src]
        src_vertex_original: LabeledDot | Mobject = src_vertex.copy()
        adjacents = [adj for adj, _ in adjacents_with_weight]

        rects: List[Rectangle] = []
        base_rect = (
            Rectangle(
                PINK,
                self.highlight_rectangle.width * 0.9,
                self.highlight_rectangle.height * 0.9,
            )
            .move_to(self.node_label_center(src))
            .set_color_by_gradient(PINK, AS2700.B21_ULTRAMARINE)
        )

        [rects.append(base_rect.copy()) for _ in adjacents]
        self.play(
            FadeIn(base_rect.set_color(GREEN_C)),
            src_vertex.animate.set_fill(RED),
            run_time=0.5,
        )
        anims = []
        for rect, adj_vertex in zip(rects, adjacents):
            anims.append(rect.animate.move_to(self.node_label_center(adj_vertex)))
        self.play(AnimationGroup(anims), run_time=1.0)

        return (
            lambda: self.play(
                src_vertex.animate.become(src_vertex_original),
                base_rect.animate.set_color(PINK),
                *[FadeOut(rect) for rect in rects],
                run_time=0.5,
            ),
            src,
            base_rect,
        )

    def get_path_resolution_animation(self) -> List[ReplacementTransform]:
        v_start = self.dijkstra.target_vertex
        if v_start is None:
            raise Exception("Unexpected case : Target vertex is None")
        anims: List[ReplacementTransform] = []
        for v_start, v_to_source in self.dijkstra.return_vertex.items():
            if v_to_source is None:
                break
            _mathtex, val, old_arrow = self.vertex_weights[v_start]
            new_arrow = (
                self.arrow_at(v_to_source, v_start, False)
                .set_color(AS2700.B23_BRIGHT_BLUE)
                .set_stroke(AS2700.B23_BRIGHT_BLUE, 12)
            )
            anims.append(ReplacementTransform(old_arrow, new_arrow))
            self.vertex_weights[v_start] = (
                _mathtex,
                val,
                new_arrow,
            )  # Update the object to properly reflec the scene's state
            v_start = v_to_source
        return anims

    def arrow_at(self, from_v: Vertex, to_v: Vertex, short: bool = True) -> Arrow:
        start = self.g.vertices[from_v].get_center()
        end = self.g.vertices[to_v].get_center()
        if short:
            end = end + (start - end) * 0.65
        else:
            end = end
        return Arrow(start, end, color=RED_E, max_tip_length_to_length_ratio=0.8)

    def get_unique_edges(self) -> Set[Edge]:
        return unique_edges(self.dijkstra.graph.edges)

    def get_unique_edges_vertexes(self) -> Set[Tuple[Vertex, Vertex]]:
        return set([(edge.from_v, edge.to_v) for edge in self.get_unique_edges()])


def dijkstra_func_1() -> Tuple[Dijkstra, int]:

    # Should be the map below
    # https://www.youtube.com/watch?v=EFg3u_E6eHU
    map = GraphMap()
    vertexes: list[Tuple[Vertex, Tuple[float, float, float]]] = [
        (Vertex(1), (0, 0, 0)),
        (Vertex(3), (1, 1.5, 1)),
        (Vertex(6), (1, -1, -1)),
        (Vertex(5), (2, 0, 1.5)),
        (Vertex(4), (3, 1.5, -0.5)),
        (Vertex(7), (3, -1.2, -1.5)),
        (Vertex(2), (4, 0, 1.2)),
    ]
    vertexes = [(v, (x * 1, y * 1, z * 1)) for v, (x, y, z) in vertexes]
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

    dijkstra = Dijkstra.new(map, 1, 2)
    steps = 300  # Some arbitrary step amount
    if dijkstra is None:
        raise Exception("Map is None")

    return (dijkstra, steps)


def dijkstra_func_2() -> Tuple[Dijkstra, int]:

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

    dijkstra = Dijkstra.new(map, 19, 5)
    steps = 500  # Some arbitrary step amount
    if dijkstra is None:
        raise Exception("Map is None")

    return (dijkstra, steps)


Manim_Dijkstra().render(True)
