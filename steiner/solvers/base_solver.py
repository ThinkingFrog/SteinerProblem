from abc import ABC, abstractmethod
from typing import List, Tuple

import networkx as nx


class BaseSolver(ABC):
    @abstractmethod
    def solve(self, graph: nx.Graph, terminals: List[int]) -> Tuple[nx.Graph, int]:
        pass
