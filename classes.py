from __future__ import annotations
from typing import Any
import matplotlib.pyplot as plt
import networkx as nx
import community

class _Vertex:
    """A vertex in a book review graph, used to represent a user or a book.

    Each vertex item is either a user id or book title. Both are represented as strings,
    even though we've kept the type annotation as Any to be consistent with lecture.

    Instance Attributes:
        - item: The data stored in this vertex, representing a user or book.
        - kind: The type of this vertex: 'user' or 'book'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'user', 'book'}
    """
    item: Any
    neighbours: set[_Vertex]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'user', 'book'}
        """
        self.item = item
        self.neighbours = set()

class Graph:
    """A graph used to represent a book review network.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx

    def make_community_graph(self, communities: dict) -> Graph:
        """
        This method shows the social network visually, highlighting the communities in the network
        """
        g = self.to_networkx()
        pos = nx.spring_layout(g)
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        nx.draw_networkx_nodes(g, pos, node_size=600, cmap=plt.cm.get_cmap('RdYlBu'),
                               node_color=list(communities.values()))
        nx.draw_networkx_edges(g, pos, alpha=0.3)
        nx.draw_networkx_labels(g, pos)
        plt.show()
        return g

    def one_community(self, communities: dict, num: int) -> Graph:
        """
        This method shows the social network with one community highlighted above others

        Preconditions:
        - 0 <= num < len(communities)
        """
        vertex_size = []
        g = self.to_networkx()
        pos = nx.spring_layout(g)
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        for node, community in communities.items():
            if community == num:
                vertex_size.append(900)
            else:
                communities[node] = 0
                vertex_size.append(300)
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        nodes = nx.draw_networkx_nodes(g, pos, node_size=vertex_size, cmap=plt.colormaps.get_cmap('winter'),
                                       node_color=list(communities.values()))
        nx.draw_networkx_edges(g, pos, alpha=0.3)
        nx.draw_networkx_labels(g, pos)
        plt.show()
        return g

def get_length(communities:list[set]) ->int:
    """Returns the number of communities in the network
    """
    return len(communities)

def test():
    """
    Test function
    """
    G = nx.karate_club_graph()  # load a default graph

    pos = nx.spring_layout(G)  # compute graph layout
    plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
    plt.axis('off')
    nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.colormaps.get_cmap('RdYlBu'), node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    nx.draw_networkx_labels(G, pos)
    plt.show()
    return G
