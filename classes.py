from __future__ import annotations
from typing import Any, Union
import matplotlib.pyplot as plt
import networkx as nx
from visualization_helper import set_to_dict


class _Vertex:
    """A vertex in a social network graph, used to represent a user.

   Each vertex item is a user id, represented as intergers,
   though we've kept the type annotation as Any to be consistent with lecture and for testing purposes.

   Instance Attributes:
       - item: The data stored in this vertex, representing a user id
       - neighbours: The vertices that are adjacent to this vertex (mutual connections) mapped to their edgeweight.

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
    vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, item: Any) -> None:
        """Add a vertex with the given item to the graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if item not in self.vertices:
            self.vertices[item] = _Vertex(item)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_inner_edge_weights(self, community: dict[int, _Vertex]) -> int:
        """
       Return the sum of edge weights in a given community set.

       Recall, when community members are all vertices edge weights are 1. COME BACK

       Preconditions:
           - all(community[v] in self.vertices for v in community)
           - list(communites.values()) == sorted(communites.values())

       >>> g = WeightedGraph()
       >>> for i in range(1, 4):
       ...     g.add_vertex(i)
       >>> g.add_edge(1, 2)
       >>> g.add_edge(2, 3)
       >>> g.add_edge(1, 3)
       >>> comm = {1: g.vertices[1], 2: g.vertices[2]}
       >>> g.get_inner_edge_weights(comm)
       1
       >>> comm = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
       >>> g.get_inner_edge_weights(comm)
       3
       >>> g.add_vertex(4)
       >>> g.add_edge(3, 4)
       >>> g.get_inner_edge_weights(comm)
       3
       >>> comm = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3], 4: g.vertices[4]}
       >>> g.get_inner_edge_weights(comm)
       4
       """
        edges_sum = 0
        edge_visited = self.create_edges_dict()  # use dictionary to improve runtime

        for v in community:
            vertex = community[v]
            for u in vertex.neighbours:
                # if {vertex, u} not in edge_visited and u.item in community:
                if u.item not in edge_visited[v] and v not in edge_visited[u.item] and u.item in community:
                    edges_sum += 1

                edge_visited[u.item].add(v)
                edge_visited[v].add(u.item)

        return edges_sum

    def get_all_outer_edges(self, communities_lst: list[dict[int, _Vertex]]) -> list[set]:
        """
       Return a list of all outer edges in a graph given a list of communities.
       Each element is a community represented as its own dictionary where the item maps to the _Vertex object.

       Note: an outer edge is an edge between vertices that are in different communities

       Preconditions:
           - all vertices/communites in the dictionaries are in self.vertices

        >>> g = WeightedGraph()
        >>> for i in range(1, 6):
        ...     g.add_vertex(i)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(1, 3)
        >>> g.add_edge(3, 4)
        >>> g.add_edge(4, 5)
        >>> g.add_edge(5, 2)
        >>> community1 = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
        >>> community2 = {4: g.vertices[4], 5: g.vertices[5]}
        >>> lst = g.get_all_outer_edges([community1, community2])
        >>> lst == [{3, 4}, {5, 2}] or lst == [{2, 5}, {3, 4}]
        True
        """
        all_outer_edges = []

        for c in communities_lst:
            all_outer_edges.extend([edge for edge in self.get_outer_edges(c) if edge not in all_outer_edges])

        return all_outer_edges

    def get_outer_edges(self, community: dict[int, _Vertex]) -> list[set]:
        """
        Returns a list of sets, where the sets are outer edges, meaning the edges between vertices/communities of
        different communities.

        Preconditions:
            - all(community[v] in self.vertices for v in community)
            - list(communites.values()) == sorted(communites.values())

        >>> g = WeightedGraph()
        >>> for i in range(1, 5):
        ...     g.add_vertex(i)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(2, 3)
        >>> g.add_edge(1, 3)
        >>> g.add_edge(3, 4)
        >>> comm = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
        >>> g.get_outer_edges(comm)
        [{3, 4}]
        """
        outer_edges = []
        edge_visited = self.create_edges_dict()

        for v in community:
            vertex = community[v]
            for u in vertex.neighbours:
                if u.item not in edge_visited[v] and v not in edge_visited[u.item] and u.item not in community:
                    outer_edges.append({v, u.item})

                edge_visited[u.item].add(v)
                edge_visited[v].add(u.item)

        return outer_edges

    def make_community_dicts(self, communities: dict[int, int]) -> list[dict[int, _Vertex]]:
        """
        Return a list of all the communites with its members in dictionaries with the item
        as the key and the _Vertex object as the value.

        Preconditions:
            - all(community[v] in self.vertices for v in community)
            - list(communites.values()) == sorted(communites.values())

        >>> communities_dict = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2}
        >>> g = WeightedGraph()
        >>> for i in range(1, 6):
        ...     g.add_vertex(i)
        >>> lst = g.make_community_dicts(communities_dict)
        >>> lst == [{1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}, {4: g.vertices[4]}, {5: g.vertices[5]}]
        True
        """
        community_ids = list(set(communities.values()))
        curr_id = community_ids[0]
        dict_lst = []
        community_dict = {}

        for v in communities:
            if communities[v] != curr_id:
                curr_id = communities[v]
                dict_lst.append(community_dict)
                community_dict = {}

            if communities[v] == curr_id:
                community_dict[v] = self.vertices[v]

        dict_lst.append(community_dict)

        return dict_lst

    def to_networkx(self) -> nx.Graph:
        """Convert this graph into a networkx Graph.
           Credit: this function is adapted from exercise 4 of CSC111, with some changes.
        """
        graph_nx = nx.Graph()
        for v in self.vertices.values():
            graph_nx.add_node(v.item)

            for u in v.neighbours:
                graph_nx.add_node(u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

        return graph_nx

    def make_community_graph(self, communities: list[set]) -> Graph:
        """
        This method shows the social network visually, highlighting the communities in the network
        """
        comms = set_to_dict(communities)
        g = self.to_networkx()
        pos = nx.spring_layout(g)
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        nx.draw_networkx_nodes(g, pos, node_size=600, cmap=plt.cm.get_cmap('RdYlBu'),
                               node_color=list(comms.values()))
        nx.draw_networkx_edges(g, pos, alpha=0.3)
        nx.draw(g, with_labels=True)
        return g

    def one_community(self, communities: list[set], num: int) -> Graph:
        """
        This method shows the social network with one community highlighted above others

        Preconditions:
        - 0 <= num < len(communities)
        """
        comms = set_to_dict(communities)
        vertex_size = []
        g = self.to_networkx()
        pos = nx.spring_layout(g)
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        for node, community in comms.items():
            if community == num:
                vertex_size.append(900)
            else:
                comms[node] = 0
                vertex_size.append(300)
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        nodes = nx.draw_networkx_nodes(g, pos, node_size=vertex_size, cmap=plt.colormaps.get_cmap('winter'),
                                       node_color=list(comms.values()))
        nx.draw_networkx_edges(g, pos, alpha=0.3)
        nx.draw(g, with_labels=True)
        return g

    def make_adjacent_matrix(self) -> dict[int, dict[int, int]]:
        """
        Make the adjacent matrix used for Louvain calculation, 1 if there's an edge between the vertices, 0 otherwise.
        """
        matrix = {}
        for v in self.vertices.values():
            matrix[v.item] = {}
            for u in self.vertices.values():
                if u in v.neighbours:
                    matrix[v.item][u.item] = 1
                else:
                    matrix[v.item][u.item] = 0

        return matrix

    def get_num_edges(self) -> int:
        """Return the number of edges in a graph."""

        total_degree = 0

        for vertex in self.vertices.values():
            total_degree += len(vertex.neighbours)

        # since undirected graph
        return int(total_degree / 2)

    def calculate_modularity_each(self, v: _Vertex, communities: dict[_Vertex, int],
                                  adjacency_matrix: dict[int, dict[int, int]], m: int) -> float:
        """
        Return the modularity of the current partitioning of communities in graph.
        Preconditions:
            - m != 0
        """
        k_v = len(v.neighbours)
        total_sum = 0

        for u in self.vertices.values():
            if communities[v] == communities[u]:
                delta = 1
            else:
                delta = 0
            k_u = len(u.neighbours)

            adjacent_score = adjacency_matrix[v.item][u.item]

            if adjacent_score != -1 and u != v:
                adjacent = (adjacent_score - (k_u * k_v) / (2 * m)) * delta
                total_sum += adjacent

        return total_sum

    def calculate_modularity_graph(self, communities: dict[_Vertex, int],
                                   adjacency_matrix: dict[int, dict[int, int]]) -> float:
        """
        Return the modularity score of the graph based on current communities.
        """
        m = self.get_num_edges()
        curr_modularity = 0

        if m > 0:
            for v in self.vertices.values():
                curr_modularity += self.calculate_modularity_each(v, communities, adjacency_matrix, m)

            return curr_modularity / (2 * m)
        else:
            return 0

    def create_edges_dict(self) -> dict[int, set]:
        """
        Return a dictionary with all vertices/communities item attributes as keys and empty sets as values.
        """
        dictionary = {}
        for v in self.vertices:
            dictionary[v] = set()

        return dictionary


class _WeightedVertex(_Vertex):
    """A vertex in a social network graph.

        Instance Attributes:
            - item: The data stored in this vertex, representing a user id
            - neighbours: The vertices that are adjacent to this vertex (mutual connections) mapped to their edgeweight.

        Representation Invariants:
            - self not in self.neighbours
            - all(self in u.neighbours for u in self.neighbours)

        """
    item: Any
    neighbours: dict[_Vertex, Union[int, float]]

    def __init__(self, item: Any) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.
        """
        super().__init__(item)
        self.item = item
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)


class _Community(_WeightedVertex):
    """
    A community in a social network graph, used to represent a group of vertices/users

    Every _Community has a community id represented as an integer.

    Instance Attributes:
        - item: the unique integer id of the community
        - neighbours: the vertices/communities that are adjacent to this community mappeded to their edge weight
        - weight: the number of edges within the community
        - members: the dictionary of the vertices/nodes items within the community mapped to their
        _Vertex/_Community object
    """
    item: Any
    neighbours: dict[_Community, Union[int, float]]
    inner_weight: int
    members: dict[int, _WeightedVertex]

    def __init__(self, item: Any, weight: int, members: dict[int, _WeightedVertex]):
        """
        Initialize a new community formed after all community members identified in previous graph.

        A community is initialized with no neighbours.
        """
        super().__init__(item)
        self.inner_weight = 2 * weight
        self.members = members


class WeightedGraph(Graph):
    """
    A graph used to represent a social media network.

    Credit: Large portion of methods and docstrings taken from Exercise 3
    """
    # Private Instance Attributes:
    #     - vertices:
    #         A collection of the vertices contained in this graph.
    #         Mapping from id to _Community
    vertices: dict[int, _WeightedVertex]

    def __init__(self) -> None:
        """
        Initialize an empty graph with no vertices, communities or edges.
        """
        super().__init__()
        self.vertices = {}

    def add_vertex(self, item: Any) -> None:
        """
        Add a vertex with the given item to this graph.

        The new _Vertex object is not adjacent to any other vertices.
        Do not do anything if the given item is already in this graph.

        Credit: method and docstring taken from Exercise 3
        """
        if item not in self.vertices:
            self.vertices[item] = _WeightedVertex(item)

    def add_community(self, item: Any, weight: int, members: dict[int: _Vertex]) -> None:
        """
        Add a community with a given item and community members to this graph.

        New community is not adjacent to anything.
        Does nothing if community is already in the graph.
        """
        if item not in self.vertices:
            self.vertices[item] = _Community(item, weight, members)

    def add_edge(self, item1: Any, item2: Any, weight: Union[int, float] = 1) -> None:
        """
        Add an edge between the two vertices/communities with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices/communities in this graph.

        Preconditions:
            - item1 != item2

        Credit: method and docstring taken from Exercise 3
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            v2 = self.vertices[item2]

            v1.neighbours[v2] = weight
            v2.neighbours[v1] = weight
        else:
            raise ValueError

    def get_weight(self, item1: Any, item2: Any) -> Union[int, float]:
        """
         Return the weight of the edge between the given items.

         Return 0 if item1 and item2 are not adjacent.

         Preconditions:
             - item1 and item2 are vertices in this graph

         Credit: method and docstring taken from Exercise 3
         """
        v1 = self.vertices[item1]
        v2 = self.vertices[item2]
        return v1.neighbours.get(v2, 0)

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """
        Return whether item1 and item2 are adjacent vertices/communities in this graph.

        Return False if item1 or item2 do not appear as vertices/communities in this graph.

        Credit: method and docstring taken from Exercise 3
        """
        if item1 in self.vertices and item2 in self.vertices:
            v1 = self.vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """
        Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex/community in this graph.

        Credit: method and docstring taken from Exercise 3
        """
        if item in self.vertices:
            v = self.vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self) -> set:
        """
        Return a set of all vertex items in this graph.

        Credit: method and docstring taken from Exercise 3
        """
        return set(self.vertices.keys())

    def to_networkx(self) -> nx.Graph:
        """
        Convert this graph into a networkx Graph.
        Credit: this function is adapted from exercise 4 of CSC111, with some changes.
        """
        graph_nx = nx.Graph()
        for v in self.vertices.values():
            graph_nx.add_node(v.item)

            for u in v.neighbours:
                graph_nx.add_node(u.item)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

        return graph_nx

    def make_community_dicts(self, communities: dict[int, int]) -> list[dict[int, _Vertex]]:
        """
        Return a list of all the communities with its memebers in separate dictionaries with the item
        as the key and the _vertex object as the value
        >>> communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2}
        >>> g = WeightedGraph()
            >>> for i in range(1, 6):
            ...     g.add_vertex(i)
        >>> lst = g.make_community_dicts(communities)
        >>> lst == [{1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}, {4: g.vertices[4]}, {5: g.vertices[5]}]
        True
        """
        community_ids = list(set(communities.values()))
        curr_id = community_ids[0]
        dict_lst = []
        community_dict = {}

        for v in communities:
            if communities[v] != curr_id:
                curr_id = communities[v]
                dict_lst.append(community_dict)
                community_dict = {}

            if communities[v] == curr_id:
                community_dict[v] = self.vertices[v]

        dict_lst.append(community_dict)

        return dict_lst

    def make_adjacent_matrix(self) -> dict[int, dict[int, int]]:
        """
        Make the adjacent "matrix" used for Louvain calculation. Stored as dictionary for easier access.
        matrix[v.item][u.item] represent edge weight between the two vertices.
        """
        matrix = {}
        for v in self.vertices.values():
            matrix[v.item] = {}
            for u in self.vertices.values():
                if u in v.neighbours:
                    matrix[v.item][u.item] = v.neighbours[u]
                else:
                    matrix[v.item][u.item] = 0

        return matrix

    def get_all_edge_weights(self) -> int:
        """
        Return the sum of all edge weights in the graph.
        Preconditions:
            - len(self.vertices) > 1
            - at least 1 edge exist in the graph
        """
        all_edge_weights = 0

        for v in self.vertices.values():
            all_edge_weights += sum(list(v.neighbours.values()))

        return int(all_edge_weights / 2)

    def calculate_modularity_each(self, v: _WeightedVertex, communities: dict[_Vertex, int],
                                  adjacency_matrix: dict[int, dict[int, int]], m: int) -> float:
        """
        Return the modularity of the current partitioning of communities in graph
        Preconditions:
            - m != 0
        """
        k_v = sum(list(v.neighbours.values()))
        total_sum = 0

        for u in self.vertices.values():
            if communities[v] == communities[u]:
                delta = 1
            else:
                delta = 0
            k_u = sum(list(u.neighbours.values()))

            adjacent_score = adjacency_matrix[v.item][u.item]

            if adjacent_score != -1 and u != v:
                adjacent = (adjacent_score - (k_u * k_v) / (2 * m)) * delta
                total_sum += adjacent
        return total_sum

    def calculate_modularity_graph(self, communities: dict[_Vertex, int],
                                   adjacency_matrix: dict[int, dict[int, int]]) -> float:
        """
        Return the modularity score of the graph based on current communities.

        Preconditions:
            - len(self.vertices) > 1
            - self.get_num_edges() > 0
        """
        m = self.get_all_edge_weights()
        curr_modularity = 0

        if m > 0:
            for v in self.vertices.values():
                curr_modularity += self.calculate_modularity_each(v, communities, adjacency_matrix, m)

            return curr_modularity / (2 * m)
        else:
            # return 0 when there's no edges between graphs
            return 0


# none class functions
def get_weighted_graph(g: WeightedGraph, communities: dict[int, int]) -> WeightedGraph:
    """
    Return the weighted graph given the dictionary of communites, where each community is one vertex

    The community id will be a tuple with the sum of edge weights in the community and an identifying integer

    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> g = WeightedGraph()
    >>> for i in range(1, 6):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> g.add_edge(2, 5)
    >>> a_new_g = get_weighted_graph(g, ex_communities)
    >>> a_new_g.get_weight(0, 1)
    2
    """
    communities_lst = g.make_community_dicts(communities)
    new_g = WeightedGraph()
    outer_edges = get_all_outer_edges(communities_lst)

    for c in communities_lst:
        inner_edge_weight = get_inner_edge_weights(c)
        new_g.add_community(get_comm_id(communities, c), inner_edge_weight, c)

    new_outer_edges = get_edge_weights(communities, outer_edges)

    for edges in new_outer_edges:
        weight = edges[1]
        comm_ids = edges[0]

        new_g.add_edge(comm_ids[0], comm_ids[1], weight)

    return new_g


def get_comm_id(all_communities: dict[int, int], community: [int, _Vertex]):
    """
    Return the id of a community
    """
    for c in community:
        return all_communities[c]


def get_all_outer_edges(communities_lst: list[dict[int, _Vertex]]) -> list[set]:
    """
    Return a list of all outer edges in a graph given a list of communities
    >>> g = WeightedGraph()
    >>> for i in range(1, 6):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> g.add_edge(4, 5)
    >>> g.add_edge(5, 2)
    >>> community1 = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
    >>> community2 = {4: g.vertices[4], 5: g.vertices[5]}
    >>> lst = get_all_outer_edges([community1, community2])
    >>> lst == [{3, 4}, {5, 2}] or lst == [{2, 5}, {3, 4}]
    True
    """
    all_outer_edges = []

    for c in communities_lst:
        all_outer_edges.extend([edge for edge in get_outer_edges(c) if edge not in all_outer_edges])

    return all_outer_edges


def get_outer_edges(community: dict[int, _Vertex]) -> list[set]:
    """
    Returns a list of sets, where the sets are outer edges

    >>> g = WeightedGraph()
    >>> for i in range(1, 5):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> g.add_edge(3, 4)
    >>> community = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
    >>> get_outer_edges(community)
    [{3, 4}]
    """
    outer_edges = []
    edge_visited = []  # improve runtime?
    for v in community:
        vertex = community[v]
        for u in vertex.neighbours:
            if {vertex, u} not in edge_visited and u.item not in community:
                outer_edges.append({v, u.item})

            edge_visited.append({vertex, u})

    return outer_edges


def get_inner_edge_weights(community: dict[int, _Vertex]) -> int:
    """
    Return sum of edge weights in a given community set

    >>> g = WeightedGraph()
    >>> for i in range(1, 4):
    ...     g.add_vertex(i)
    >>> g.add_edge(1, 2)
    >>> g.add_edge(2, 3)
    >>> g.add_edge(1, 3)
    >>> a_community = {1: g.vertices[1], 2: g.vertices[2]}
    >>> get_inner_edge_weights(a_community)
    1
    >>> a_community = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3]}
    >>> get_inner_edge_weights(a_community)
    3
    >>> g.add_vertex(4)
    >>> g.add_edge(3, 4)
    >>> get_inner_edge_weights(community)
    3
    >>> a_community = {1: g.vertices[1], 2: g.vertices[2], 3: g.vertices[3], 4: g.vertices[4]}
    >>> get_inner_edge_weights(a_community)
    4
    """
    edges_sum = 0
    edge_visited = []  # improve runtime with dictionary?
    for v in community:
        vertex = community[v]
        for u in vertex.neighbours:
            if {vertex, u} not in edge_visited and u.item in community:
                edges_sum += 1

            edge_visited.append({vertex, u})

    return edges_sum


def get_edge_weights(communities: dict[int, int], outer_edges: list[set]) -> list[tuple[list[int], int]]:
    """
    Return a dictionary of edges with their new community ids and weights.
    Within the tuple, the edges are represented as a list with each element being a vertices and the edge weight is
    represented as an integer.

    As follows: ([community1 id, community2 id], weight)

    Preconditions
        - list(communites.values()) == sorted(communites.values())
        - every e in outer edges is an existing edge in a graph

    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2}
    >>> outer_e = [{5, 2}, {4, 3}]
    >>> get_edge_weights(ex_communities, outer_e)
    [([0, 2], 1), ([0, 1], 1)]
    >>> ex_communities = {1: 0, 2: 0, 3: 0, 4: 1, 5: 1}
    >>> get_edge_weights(ex_communities, outer_e)
    [([0, 1], 2)]
    """
    edges_dict = {}
    for edge in outer_edges:
        edge_name = set()
        for v in edge:
            edge_name.add(communities[v])

        edge_name = frozenset(edge_name)

        if edge_name in edges_dict:
            edges_dict[edge_name] += 1
        else:
            edges_dict[edge_name] = 1

    return [(list(key), edges_dict[key]) for key in edges_dict]