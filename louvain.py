from classes import _Community, WeightedGraph

def aggregate_communities_from_vertex(all_communities: set[frozenset[int]]) -> (WeightedGraph, set[_Community]):
    """
    The initial function that aggregates a set of _Vertex.
    Form a set of communities (_Community class) and a graph representing the relationship between the communities.
    Will only be called once.
    """
    # TODO

def aggregate_communities(all_communities: set[_Community]) -> (WeightedGraph, set[_Community]):
    """
    The function that aggregates communities from communities.
    Form a set of communities (_Community class) and a graph representing the relationship between communities.
    """
    # TODO
