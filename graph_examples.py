from graph import Graph


def from_edges(edges: list[tuple[int, int, int]], /) -> Graph:
    result = Graph()
    for source, target, weight in edges:
        result.add_edge(source, target, weight)
    return result


def empty_graph() -> Graph:
    return Graph()


def isolated_vertices_graph(vertex_count: int, /) -> Graph:
    result = Graph()
    for vertex in range(vertex_count):
        result.add_vertex(vertex)
    return result


def path_graph(vertex_count: int, /, *, weight: int = 1, directed: bool = True) -> Graph:
    result = isolated_vertices_graph(vertex_count)
    for source in range(vertex_count - 1):
        result.add_edge(source, source + 1, weight)
        if not directed:
            result.add_edge(source + 1, source, weight)
    return result


def cycle_graph(vertex_count: int, /, *, weight: int = 1, directed: bool = True) -> Graph:
    result = path_graph(vertex_count, weight=weight, directed=directed)
    if vertex_count > 1:
        result.add_edge(vertex_count - 1, 0, weight)
        if not directed:
            result.add_edge(0, vertex_count - 1, weight)
    return result


def complete_graph(vertex_count: int, /, *, weight: int = 1, directed: bool = True) -> Graph:
    result = isolated_vertices_graph(vertex_count)
    for source in range(vertex_count):
        for target in range(vertex_count):
            if source == target:
                continue
            if directed:
                result.add_edge(source, target, weight)
            elif source < target:
                result.add_edge(source, target, weight)
                result.add_edge(target, source, weight)
    return result


def grid_graph(row_count: int, column_count: int, /, *, weight: int = 1, directed: bool = True) -> Graph:
    result = isolated_vertices_graph(row_count * column_count)
    for row in range(row_count):
        for column in range(column_count):
            vertex = row * column_count + column
            if column + 1 < column_count:
                result.add_edge(vertex, vertex + 1, weight)
                if not directed:
                    result.add_edge(vertex + 1, vertex, weight)
            if row + 1 < row_count:
                result.add_edge(vertex, vertex + column_count, weight)
                if not directed:
                    result.add_edge(vertex + column_count, vertex, weight)
    return result


def weighted_graph() -> Graph:
    return from_edges([
        (0, 1, 4),
        (0, 7, 8),
        (1, 2, 8),
        (1, 7, 11),
        (2, 3, 7),
        (2, 5, 4),
        (2, 8, 2),
        (3, 4, 9),
        (3, 5, 14),
        (4, 5, 10),
        (5, 6, 2),
        (6, 7, 1),
        (6, 8, 6),
        (7, 8, 7),
    ])


def disconnected_graph() -> Graph:
    return from_edges([
        (0, 1, 4),
        (1, 2, 1),
        (2, 0, 3),
        (3, 4, 7),
        (4, 5, 2),
        (5, 3, 5),
    ])


def graph_with_unreachable_vertex() -> Graph:
    result = from_edges([
        (0, 1, 2),
        (1, 2, 3),
        (2, 3, 1),
    ])
    result.add_vertex(4)
    result.add_vertex(5)
    return result


def graph_with_zero_weights() -> Graph:
    return from_edges([
        (0, 1, 0),
        (1, 2, 0),
        (0, 2, 5),
        (2, 3, 0),
        (3, 4, 2),
    ])


def graph_with_negative_weight() -> Graph:
    return from_edges([
        (0, 1, 5),
        (1, 2, -3),
        (2, 3, 2),
    ])


def graph_with_self_loops() -> Graph:
    return from_edges([
        (0, 0, 3),
        (0, 1, 2),
        (1, 1, 7),
        (1, 2, 1),
        (2, 2, 0),
    ])
