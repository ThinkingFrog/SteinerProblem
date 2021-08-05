from dataclasses import dataclass


@dataclass
class GraphInfo:
    name: str = ""
    cost: int = 0
    nodes: int = 0
    edges: int = 0
    terminals: int = 0
