from pathlib import Path
from typing import List


class Config:
    _data = List[Path]
    _output: Path

    def __init__(self, path_to_data: Path, path_to_output: Path) -> None:
        path_to_output.mkdir(parents=True, exist_ok=True)
        self._output = path_to_output

        self._data = list()

        if not path_to_data.is_dir():
            self._data.append(path_to_data)
        else:
            for graph_path in path_to_data.rglob("*.stp"):
                self._data.append(graph_path)

    def data(self) -> List[Path]:
        return self._data

    def output(self) -> Path:
        return self._output
