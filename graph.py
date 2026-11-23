class Graph:
    """
    Реализация ориентированного взвешенного графа; петли разрешены, параллельные рёбра — нет.
    Вершины представляются числами (``int``), рёбра — ``tuple[int, int]``.
    """

    def __init__(self, /):
        """Создаёт пустой граф"""
        self._structure: dict[int, set[int]] = {}
        self._weights: dict[tuple[int, int], int] = {}

    def get_vertices(self, /) -> set[int]:
        """Возращает множество всех вершин графа"""
        return {vertex for vertex in self._structure.keys()}

    def get_sources(self, target: int, /) -> set[int]:
        """Возращает множество вершин, у которых есть ребро, ведущее в ``target``"""
        return {vertex for vertex in self._structure if target in self._structure[vertex]}

    def get_targets(self, source: int, /) -> set[int]:
        """Возращает множество вершин, у которых есть ребро, исходящее из ``source``"""
        return {target for target in self._structure.get(source, set())}

    def get_edges(self, /) -> set[tuple[int, int]]:
        """Возращает множество рёбер графа"""
        return {(source, target) for source in self.get_vertices() for target in self.get_targets(source)}

    def get_income_edges(self, target: int, /) -> set[tuple[int, int]]:
        """Возращает множество входящих в ``target`` рёбер"""
        return {(source, target) for source in self.get_sources(target)}

    def get_outcome_edges(self, source: int, /) -> set[tuple[int, int]]:
        """Возращает множество исходящих из ``source`` рёбер"""
        return {(source, target) for target in self.get_targets(source)}

    def get_weight(self, source: int, target: int, /) -> int | None:
        """Возращает вес ребра, идущего из ``source`` в ``target``; ``None`` если такого ребра нет"""
        return self._weights.get((source, target), None)

    def add_vertex(self, vertex: int, /):
        """Добавляет новую вершину ``vertex`` в граф; ничего не делает, если такая вершина уже есть"""
        self._structure.setdefault(vertex, set())

    def add_edge(self, source: int, target: int, weight: int, /):
        """Добавляет новое ребро в граф, идущее из ``source`` в ``target`` с весом ``weight``; обновляет вес, если такое ребро уже есть"""
        self.add_vertex(source)
        self.add_vertex(target)
        self._structure[source].add(target)
        self._weights[(source, target)] = weight

    def remove_edge(self, source: int, target: int, /):
        """Удаляет ребро из графа, идущее из ``source`` в ``target``; ничего не делает, если такого ребро нет"""
        self._structure.get(source, set()).discard(target)
        self._weights.pop((source, target), None)

    def remove_vertex(self, vertex: int, /):
        """Удаляет вершину ``vertex`` из графа; ничего не делает, если такой вершины нет"""
        for source in self.get_sources(vertex):
            self.remove_edge(source, vertex)
        for target in self.get_targets(vertex):
            self.remove_edge(vertex, target)
        self._structure.pop(vertex, None)
