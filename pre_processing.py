from classes import Graph
import csv


def get_graph(vertices: str, edges: str) -> (Graph, dict[str, str]):
    """
    Create graph from the files.
    vertices is the file full of vertices, and edges being the path to fie of edges.
    """
    identifier = 0  # identifier for duplicates, value does not matter, just to distinguish nodes
    g = Graph()
    all_data_vertices = {}
    with open(vertices, mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] in all_data_vertices.values():
                all_data_vertices[int(row[2])] = row[1] + str(identifier)
                identifier += 1
            else:
                all_data_vertices[int(row[2])] = row[1]

            g.add_vertex(int(row[2]))

    with open(edges, mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        valid_vertices = [key for key in all_data_vertices]
        for row in reader:
            if all(int(vertex) in valid_vertices for vertex in row):
                g.add_edge(int(row[0]), int(row[1]))

    return g, all_data_vertices
