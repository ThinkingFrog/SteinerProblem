import matplotlib.pyplot as plt
import networkx as nx


def print_graph(graph: nx.Graph) -> None:
    print(f"Graph size is {graph.size()}")
    for src, dest, weight in graph.edges.data("weight"):
        print(f"E {src} {dest} {weight}")


def draw_graph(graph: nx.Graph, title: str) -> None:
    nx.draw_networkx(graph)
    plt.title(title)
    plt.show()
