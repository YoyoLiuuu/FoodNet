from __future__ import annotations
from typing import Any
import networkx as nx


class _Vertex:
    """A vertex in an artist network graph, used to represent an artist.

    Each vertex item is the id of the artist

    Instance Attributes:
        - item: The data stored in this vertex, representing an artist.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
    """
    item: int
    neighbours: set[_Vertex]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item.

        This vertex is initialized with no neighbours.
        """
        self.item = item
        self.neighbours = set()

    def check_connected(self, target_item: Any, visited: set[_Vertex]) -> bool:
        """Return whether this vertex is connected to a vertex corresponding to the target_item,
        WITHOUT using any of the vertices in visited.
        Preconditions:
            - self not in visited
        """
        if self.item == target_item:
            # Base case: the target_item is the current vertex
            return True
        else:
            visited.add(self)  # Add self to the set of visited vertices
            for u in self.neighbours:
                if u not in visited:  # Only recurse on vertices that haven't been visited
                    if u.check_connected(target_item, visited):
                        return True

            return False


class Graph:
    """A graph used to represent an artist connection network.
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
        """Add a vertex with the given item to the graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
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

    def to_networkx(self) -> nx.Graph:
        """Convert this graph into a networkx Graph.
           Credit: this function is adapted from exercise 4 of CSC111, with some changes.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item)

            for u in v.neighbours:
                graph_nx.add_node(u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

        return graph_nx

    def make_adjacent_matrix(self) -> dict[int, dict[int, int]]:
        """
        Make the adjacent matrix used for Louvain calculation.
        """
        matrix = {}
        # make a dictionary for each vertex v such that the dictionary is in the format:
        # keys = u.item for all vertices in graph
        # values = the distance between u and v, -1 if they are not connected (if u = v, the value is 0)
        for v in self._vertices:
            matrix[v] = {}
            for u in self._vertices:
                if self._vertices[v].check_connected(u, set()):
                    matrix[v][u] = nx.shortest_path_length(self.to_networkx(60000), v, u)
                else:
                    matrix[v][u] = -1

        return matrix
