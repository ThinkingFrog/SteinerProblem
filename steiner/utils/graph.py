import matplotlib.pyplot as plt
import networkx as nx
import networkx.drawing.layout as nxdl


def print_graph(graph: nx.Graph) -> None:
    print(f"Graph size is {graph.size()}")
    for src, dest, weight in graph.edges.data("weight"):
        print(f"E {src} {dest} {weight}")


def draw_graph(graph: nx.Graph, title: str) -> None:
    pos = nxdl.spring_layout(graph)
    nx.draw_networkx(graph, pos)
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.title(title)
    plt.show()
