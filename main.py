from dijkstra import shortest_path_dijkstra
from graph_examples import (
    complete_graph,
    cycle_graph,
    disconnected_graph,
    empty_graph,
    from_edges,
    graph_with_negative_weight,
    graph_with_self_loops,
    graph_with_unreachable_vertex,
    graph_with_zero_weights,
    grid_graph,
    isolated_vertices_graph,
    path_graph,
    weighted_graph,
)

graph = empty_graph()
try:
    shortest_path_dijkstra(graph, 0)
except ValueError:
    pass
else:
    assert False, "empty graph should reject a start vertex"

graph = isolated_vertices_graph(4)
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: None, 2: None, 3: None}
assert shortest_path_dijkstra(graph, 3) == {0: None, 1: None, 2: None, 3: 0}

graph = path_graph(5)
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
assert shortest_path_dijkstra(graph, 4) == {0: None, 1: None, 2: None, 3: None, 4: 0}

graph = path_graph(4, weight=3)
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 3, 2: 6, 3: 9}

graph = path_graph(4, directed=False)
assert shortest_path_dijkstra(graph, 2) == {0: 2, 1: 1, 2: 0, 3: 1}

graph = cycle_graph(5)
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

graph = cycle_graph(4, directed=False)
assert shortest_path_dijkstra(graph, 1) == {0: 1, 1: 0, 2: 1, 3: 2}

graph = complete_graph(5, weight=3)
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 3, 2: 3, 3: 3, 4: 3}

graph = complete_graph(4, directed=False, weight=1)
assert shortest_path_dijkstra(graph, 2) == {0: 1, 1: 1, 2: 0, 3: 1}

graph = grid_graph(3, 4)
assert shortest_path_dijkstra(graph, 0) == {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 1,
    5: 2,
    6: 3,
    7: 4,
    8: 2,
    9: 3,
    10: 4,
    11: 5,
}

graph = grid_graph(2, 2, directed=False)
assert shortest_path_dijkstra(graph, 3) == {0: 2, 1: 1, 2: 1, 3: 0}

graph = weighted_graph()
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 4, 2: 12, 3: 19, 4: 28, 5: 16, 6: 18, 7: 8, 8: 14}

graph = weighted_graph()
assert shortest_path_dijkstra(graph, 4) == {
    0: None,
    1: None,
    2: None,
    3: None,
    4: 0,
    5: 10,
    6: 12,
    7: 13,
    8: 18,
}

graph = disconnected_graph()
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 4, 2: 5, 3: None, 4: None, 5: None}

graph = disconnected_graph()
assert shortest_path_dijkstra(graph, 4) == {0: None, 1: None, 2: None, 3: 7, 4: 0, 5: 2}

graph = graph_with_unreachable_vertex()
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 2, 2: 5, 3: 6, 4: None, 5: None}

graph = graph_with_unreachable_vertex()
assert shortest_path_dijkstra(graph, 4) == {0: None, 1: None, 2: None, 3: None, 4: 0, 5: None}

graph = graph_with_zero_weights()
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 0, 2: 0, 3: 0, 4: 2}

graph = graph_with_negative_weight()
try:
    shortest_path_dijkstra(graph, 0)
except ValueError:
    pass
else:
    assert False, "negative edge weight should be rejected"

graph = graph_with_self_loops()
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 2, 2: 3}

graph = from_edges([(2, 0, 1), (0, 1, 1)])
assert shortest_path_dijkstra(graph, 2) == {0: 1, 1: 2, 2: 0}
assert shortest_path_dijkstra(graph, 1) == {0: None, 1: 0, 2: None}

graph = from_edges([(0, 1, 9), (0, 2, 1), (2, 1, 1)])
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 2, 2: 1}

graph = from_edges([(0, 1, 10 ** 9), (1, 2, 10 ** 9), (0, 3, 2), (3, 2, 5)])
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 10 ** 9, 2: 7, 3: 2}

graph = from_edges([(0, 1, 1), (0, 2, 1), (0, 3, 1), (1, 2, 1)])
graph.add_vertex(4)
assert shortest_path_dijkstra(graph, 0) == {0: 0, 1: 1, 2: 1, 3: 1, 4: None}

graph = from_edges([(0, 5, 1), (5, 6, 1)])
try:
    shortest_path_dijkstra(graph, 3)
except ValueError:
    pass
else:
    assert False, "start vertex absent from graph should be rejected"

print("all tests passed")
