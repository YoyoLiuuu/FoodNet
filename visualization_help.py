def set_to_dict(communities: list[set]) -> dict:
    dct = {}
    for i in range(0, len(communities)):
        for node in communities[i]:
            dct[node] = i
    return dct


"""def test():
    """
# Test
# function
"""
G = nx.karate_club_graph()  # load a default graph

partition = community.best_partition(G)  # compute communities

pos = nx.spring_layout(G)  # compute graph layout
plt.figure(figsize=(8, 8))  # image is 8 x 8 inches
plt.axis('off')
nx.draw_networkx_nodes(G, pos, node_size=600, cmap=plt.colormaps.get_cmap('RdYlBu'), node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw(G, with_labels=True)
# plt.show(G)
return G
"""
