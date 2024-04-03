
def set_to_dict(communities: list[set]) -> dict:
    dct = {}
    for i in range(0, len(communities)):
        for node in communities[i]:
            dct[node] = i
    return dct
