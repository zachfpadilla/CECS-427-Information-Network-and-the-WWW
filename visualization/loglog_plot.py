import matplotlib as plt

def loglog_plot(graph):
    """generates a log-log plot of the in-degree distribution"""
    #get in-degrees of all nodes
    in_degrees = [d for n, d in graph.in_degree()]

    if not in_degrees:
        print("Graph is empty, cannot generate plot.")
        return

    #sort nodes
    in_degrees.sort(reverse=True)

    plt.figure(figsize=(10, 6))
    plt.loglog(in_degrees, 'b-', marker='o', markersize=4, linewidth=1, label='In-Degree')
    plt.title("Log-Log Plot of In-Degree Distribution")
    plt.xlabel("Rank (Node Index)")
    plt.ylabel("In-Degree Frequency")
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()

    print("Displaying LogLog plot...")
    plt.show()