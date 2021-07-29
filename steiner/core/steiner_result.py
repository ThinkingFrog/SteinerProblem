from typing import Dict


class SteinerResult:
    _result: Dict[str, Dict[str, int]]

    def __init__(self) -> None:
        self._result = dict()

    def add(self, graph_name: str, algorithm_name: str, tree_cost: int) -> None:
        if graph_name not in self._result.keys():
            self._result[graph_name] = dict()

        self._result[graph_name][algorithm_name] = tree_cost

    def print(self) -> None:
        for graph_name in self._result:
            print(graph_name)

            for algorithm_name in self._result[graph_name]:
                print(f"{algorithm_name}: {self._result[graph_name][algorithm_name]}")
