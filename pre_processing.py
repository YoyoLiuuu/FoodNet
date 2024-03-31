from classes import Graph
import csv


def get_graph() -> (Graph, dict[str, str]):
    g = Graph()
    all_data_vertices = {}
    matrix_value = 0
    # with open('fb-pages-artist-nodes.txt', mode='r', encoding='cp437') as file:
    with open('test_nodes.txt', mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        for row in reader:
            all_data_vertices[row[2]] = row[1]
            g.add_vertex(row[2], matrix_value)
            matrix_value += 1

    # with open('fb-pages-artist-edges.txt', mode='r', encoding='cp437') as file:
    with open('test_edges.txt', mode='r', encoding='cp437') as file:
        reader = csv.reader(file)
        valid_vertices = all_data_vertices.keys()
        for row in reader:
            if all(vertex in valid_vertices for vertex in row):
                g.add_edge(row[0], row[1])

    return g, all_data_vertices
