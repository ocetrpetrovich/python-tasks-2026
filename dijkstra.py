from typing import cast

from graph import Graph
from heap import Heap


def shortest_path_dijkstra(graph: Graph, start: int, /) -> dict[int, int | None]:
    """Возращает словарь отображающий вершину в расстояние до неё от ``start`` в графе ``graph``; -1 для недостижимых вершин"""
    if start not in graph.get_vertices():
        raise ValueError("Start vertex is not in graph")
    queue: Heap[tuple[int, int]] = Heap(key=lambda x: x[1])
    queue.push((start, 0))
    distances: dict[int, int | None] = {}
    while queue:
        source, distance = queue.pop()
        if source in distances:
            continue
        distances[source] = distance
        for target in graph.get_targets(source):
            weight = cast(int, graph.get_weight(source, target))
            if weight < 0:
                raise ValueError("Edge weight should not be negative to use Dijkstra algorithm")
            queue.push((target, distance + weight))
    for vertex in graph.get_vertices():
        if vertex not in distances:
            distances[vertex] = None
    return distances
