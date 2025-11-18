import networkx as nx
from networkx.algorithms.bipartite import is_bipartite
import numbers

def verify_bipartite_graph(G):
    if not is_bipartite(G):
        return False
    A, B = nx.bipartite.sets(G)
    all_numeric_price = all(
        isinstance(G.nodes[n].get("price"), numbers.Number)
        for n in A
    )
    all_numeric_valuation = all(
        isinstance(G.edges[e].get("valuation"), numbers.Number)
        for e in G.edges(A)
    )
    return all_numeric_price and all_numeric_valuation
