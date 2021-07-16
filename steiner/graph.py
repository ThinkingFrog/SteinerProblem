from typing import Dict, List


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

    def print(self):
        for edge in self._edges:
            print(f"E {edge['src']} {edge['dest']} {edge['weight']}")
