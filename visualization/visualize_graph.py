import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(G, matching=None):
    """Visualizes the graph based on computed metrics."""
    if G.number_of_nodes() == 0:
        print("Cannot plot an empty graph.")
        return

    print(f"Generating plot...")
    plt.figure(figsize=(12, 12))
#    A, B = nx.bipartite.sets(G)
#    pos = nx.bipartite_layout(G, A)
#
#    node_colors = ["blue" if G.nodes[node]["bipartite"] == 0  else "red" for node in G.nodes()]
#    edge_labels = nx.get_edge_attributes(G, "valuation")
#    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, "price"), node_color=node_colors, font_color='white')
#    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.7)

    #^expanded above code in order to support --interactive

    sellers = {n for n, d in G.nodes(data=True) if d['bipartite'] == 0}
    pos = nx.bipartite_layout(G, sellers)
    node_colors = ["blue" if G.nodes[node]["bipartite"] == 0 else "red" for node in G.nodes()]

    #draw base graph
    nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, "price"), node_color=node_colors,
            font_color='white')

    #draw valuations if they exist on edges
    if nx.get_edge_attributes(G, "valuation"):
        edge_labels = nx.get_edge_attributes(G, "valuation")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.7)

    #highlight the matching edges if a matching is provided
    if matching:
        matching_edges = []
        for node1, node2 in matching.items():
            if G.has_edge(node1, node2):
                matching_edges.append((node1, node2))

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=matching_edges,
            edge_color='green',
            width=2.5,
            style='dashed'
        )

    plt.show()
