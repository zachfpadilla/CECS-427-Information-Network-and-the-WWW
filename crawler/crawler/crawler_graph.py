import networkx as nx

#pass in G & args.crawler_graph
def crawler_graph(G, output_file):
    """generates a log-log plot of the in-degree distribution"""
    try:
        nx.write_gml(G, output_file)
        print(f"Crawled graph saved to {output_file}")
    except Exception as e:
        print(f"Error saving graph: {e}")