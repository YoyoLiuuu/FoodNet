from classes import Graph
import csv


def get_graph(vertices: str, edges: str) -> (Graph, dict[str, str]):
    """
    docstring
    """
    g = Graph()
    all_data_vertices = {}
    # with open('fb-pages-artist-nodes.txt', mode='r', encoding='cp437') as file:
    with open(vertices, mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        for row in reader:
            all_data_vertices[int(row[2])] = row[1]
            g.add_vertex(int(row[2]))

    # with open('fb-pages-artist-edges.txt', mode='r', encoding='cp437') as file:
    with open(edges, mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        valid_vertices = [key for key in all_data_vertices]
        for row in reader:
            if all(int(vertex) in valid_vertices for vertex in row):
                g.add_edge(int(row[0]), int(row[1]))

    return g, all_data_vertices
