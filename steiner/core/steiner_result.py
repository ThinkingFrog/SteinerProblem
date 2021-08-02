import csv
import json
from pathlib import Path
from typing import Dict, Union

import mergedeep

from steiner.core.graph_info import GraphInfo


class SteinerResult:
    _graph_data: Dict[str, Dict[str, int]]
    _algorithm_data: Dict[str, Dict[str, Dict[str, Union[int, float]]]]

    def __init__(self) -> None:
        self._graph_data = dict()
        self._algorithm_data = dict()

    def add(
        self,
        graph_info: GraphInfo,
        algorithm_name: str,
        tree_cost: int,
        runtime: float,
        valid: bool,
    ) -> None:
        if graph_info.name not in self._graph_data.keys():
            self._graph_data[graph_info.name] = dict()
            self._algorithm_data[graph_info.name] = dict()

            self._graph_data[graph_info.name]["Nodes"] = graph_info.nodes
            self._graph_data[graph_info.name]["Edges"] = graph_info.edges
            self._graph_data[graph_info.name]["Terminals"] = graph_info.terminals
            self._graph_data[graph_info.name]["Expected cost"] = graph_info.cost

        self._algorithm_data[graph_info.name][algorithm_name] = dict()

        self._algorithm_data[graph_info.name][algorithm_name][
            "Steiner tree cost"
        ] = tree_cost
        self._algorithm_data[graph_info.name][algorithm_name]["Absolute error"] = (
            tree_cost - self._graph_data[graph_info.name]["Expected cost"]
        )
        self._algorithm_data[graph_info.name][algorithm_name]["Relative error (%)"] = (
            tree_cost / self._graph_data[graph_info.name]["Expected cost"] - 1
        ) * 100
        self._algorithm_data[graph_info.name][algorithm_name]["Runtime (s)"] = runtime
        self._algorithm_data[graph_info.name][algorithm_name]["Validated"] = valid

    def write_to_json(self, json_file_path: Path) -> None:
        with json_file_path.open("w") as f:
            json.dump(
                mergedeep.merge({}, self._graph_data, self._algorithm_data), f, indent=4
            )

    def write_to_csv(self, csv_file_path: Path) -> None:
        with csv_file_path.open("w") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(
                [
                    "Graph",
                    "Algorithm",
                    *list(list(self._graph_data.values())[0].keys()),
                    *list(
                        list(list(self._algorithm_data.values())[0].values())[0].keys()
                    ),
                ]
            )

            for graph_name in self._graph_data:
                for algorithm_name in self._algorithm_data[graph_name]:
                    csv_writer.writerow(
                        [
                            graph_name,
                            algorithm_name,
                            *list(self._graph_data[graph_name].values()),
                            *list(
                                self._algorithm_data[graph_name][
                                    algorithm_name
                                ].values()
                            ),
                        ]
                    )

    def dump(self, outdir: Path):
        self.write_to_csv(outdir / "result.csv")
        self.write_to_json(outdir / "result.json")
