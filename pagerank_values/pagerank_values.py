import networkx as nx

def pagerank_values(G, output_file):
    """calculates page rank and saves to file"""
    if len(G) == 0:
        print("Graph is empty, skipping PageRank.")
        return

    print("Calculating PageRank...")
    try:
        pr_values = nx.pagerank(G, alpha=0.85)
        #sort nodes
        sorted_pr = sorted(pr_values.items(), key=lambda x: x[1], reverse=True)

        with open(output_file, 'w') as f:
            f.write(f"{'PageRank':<15} | {'URL'}\n")
            f.write("-" * 80 + "\n")
            for node, score in sorted_pr:
                f.write(f"{score:.8f}      | {node}\n")

        print(f"PageRank values saved to {output_file}")

    except Exception as e:
        print(f"Error calculating PageRank: {e}")