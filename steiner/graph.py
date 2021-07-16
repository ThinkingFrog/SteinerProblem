from typing import List, Dict


class Graph:
    _vertices: int
    _edges: List[Dict[str, int]]

    def __init__(self, V: int) -> None:
        self._vertices = V
        self._edges = list()

    @property
    def V(self):
        return self._vertices

    def add_edge(self, src: int, dest: int, weight: int):
        self._edges.append({"src": src, "dest": dest, "weight": weight})
