# CECS 427 Information Network and the WWW

#### Martin Silva (#030854159), Zachary Padilla (#033497475)

## Dependencies
In order to run this project:

```
~/: git clone https://github.com/zachfpadilla/CECS-427-Social-and-Large-Scale-Networks
~/: cd CECS-427-Social-and-Large-Scale-Networks/

### Optionally ###
~/CECS-427-Social-and-Large-Scale-Networks/: python3 -m venv .venv
~/CECS-427-Social-and-Large-Scale-Networks/: source .venv/bin/activate
(.venv) ~/CECS-427-Social-and-Large-Scale-Networks/: pip install networkx, pandas, matplotlib
```

```
~/CECS-427-Social-and-Large-Scale-Networks/: python3 ./graph_analysis.py -h

usage: graph_analysis.py [-h] [--components n] [--split_output_dir dir] [--plot {C,N,P}] [--verify_homophily] [--verify_balanced_graph] [--output output.gml]
                         [--simulate_failures k] [--robustness_check k] [--temporal_simulation FILE.CSV]
                         graph_file

Python application that handles Girvan-Newman graph partitioning, edge removal, homophily/balance verification, and visualization.

positional arguments:
  graph_file            Path to the input graph file in .gml format.

options:
  -h, --help            show this help message and exit
  --components n        Reads a graph from the given .gml file and uses it for all subsequent operations.
  --split_output_dir dir
                        Exports each component to a separate .gml file in the given directory (optional; used with --components).
  --plot {C,N,P}        Control visualization output:
                        (C)lustering coefficient (node size = CC, color = degree)
                        (N)eighborhood overlap (edge thickness= NO, color = sum of degrees at and points)
                        (P)lot the attributes e.g., node color, edge signs
  --verify_homophily    Uses a statistical test (t-test) to check homophily using color-coded node attributes.
  --verify_balanced_graph
                        Checks if the signed graph is balanced using the BFS-based methods.
  --output output.gml   Saves the final graph with all updated node/edge attributes.
  --simulate_failures k
                        Randomly removes k edges and analyzes:
                        Change in average shortest path
                        Number of disconnected components
                        Impact on betweenness centrality
  --robustness_check k  Performs multiple simulations of k random edge failures and report:
                        Average number of connected components
                        Max/min component sizes
                        Whether original clusters persist
  --temporal_simulation FILE.CSV
                        Loads a time series of edge changes in CSV format (source,target,timestamp,action) and animate the graph evolution.
```

## Usage Instructions
* ``--plot`` outputs an image of the plot to a new window.
  * When using plot, you can cantrol the visualization output by choosing between flags C, N, P.
    * ``--plot C`` visualizes the clustering coefficient, represented by node size. Additionally, a color is set to represent the degree of each node.
    * ``--plot N`` visualizes the Neighborhood Overlap through edge thickness. The color represents the sum of degrees at and points. 
    * ``--plot P`` visualizes the assigned node color and labels the sign of each edge.
* ``--components n``
  * Partition the graph into `n` components using the **Girvan-Newman** method. 
    *  Include  `--robustness_check` flag to simulate the effect of removing k random edges before partitioning.

* Allow exporting each component to a separate .gml file (optional: ``--split_output_dir``).

* ``--verify_homophily``
  * Statistical test (t-test) to check homophily using color-coded node attributes.
* ``--verify_balanced_graph``
  * ``Check if the signed graph is balanced using the BFS-based methods.``

* ``--output out_graph_file.gml``
  * Save the final graph with all updated node/edge attributes.

* ``--simulate_failures k``
  * Randomly remove k edges and analyze:
    * Change in average shortest path
    * Number of disconnected components
    * Impact on betweenness centrality

* ``--robustness_check k``
  * Perform multiple simulations of k random edge failures and report:
    * Average number of connected components
    * Max/min component sizes
    * Whether original clusters persist

* ``--temporal_simulation file.csv``
  * Load a time series of edge changes in CSV format (source,target,timestamp,action) and animate the graph evolution. 

## Description of Implementation
- All instructions were followed as listed—interpretations were made where needed.

## Examples of Commands and Outputs

``> python ./graph_analysis.py graph.gml --components 3 --plot C --simulate_failures 5 --output output.gml``
```
Successfully loaded graph from 'graph.gml'.
Nodes: 6, Edges: 6
Partitioning graph into 3 components...
Graph partitioned. Nodes are now tagged with a 'community' attribute.
--- Simulating 5 Random Edge Failures ---
Removed 5 edges.

--- Impact Analysis ---
Connected Components: 1 -> 5
Avg. Shortest Path (largest comp.): 1.9333 -> 1.0000

Top 5 Nodes by Change in Betweenness Centrality:
  - Node Alice: Change = 0.6000
  - Node Charlie: Change = 0.4000
  - Node David: Change = 0.4000
  - Node Bob: Change = 0.0000
  - Node Eve: Change = 0.0000
---------------------------

Generating plot for type: 'C'...
Computing clustering coefficients...
Done.
/home/martin/CECS-427-Social-and-Large-Scale-Networks/visualization/visualize_graph.py:47: UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown
  plt.show()

Saving final graph with new attributes to 'output.gml'...
Graph saved successfully.
```

``> python ./graph_analysis.py graph.gml --verify_homophily --verify_balanced_graph --output output.gml``
```
Successfully loaded graph from 'graph.gml'.
Nodes: 20, Edges: 46
Verifying homophily based on node attribute: 'color'...
Assortativity Coefficient (r): -0.6553
The graph shows evidence of heterophily (r < 0). Nodes tend to connect to nodes with a different 'color'.
Verifying structural balance based on edge attribute: 'sign'...
The graph is not structurally balanced. A conflict was found.

Saving final graph with new attributes to 'output.gml'...
Graph saved successfully.
```
`` python ./graph_analysis.py graph.gml --plot T --temporal_simulation edges.csv ``
```
Successfully loaded graph from 'graph.gml'.
Nodes: 20, Edges: 46
Generating plot for type: 'T'...
Starting temporal simulation with event file: edges.csv
```
<img src="https://github.com/zachfpadilla/CECS-427-Social-and-Large-Scale-Networks/blob/main/temporal_simulation.gif" />
