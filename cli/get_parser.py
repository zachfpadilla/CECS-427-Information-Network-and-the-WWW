import argparse

#def validFileName(str):
#    """Returns the filename only if it follows valid naming scheme."""
#    file_name_array = str.split('.')
#    if len(file_name_array) != 2:
#        raise argparse.ArgumentTypeError('File name requires exactly one .gml extension.')
#    if file_name_array[1] != "gml":
#        raise argparse.ArgumentTypeError('File name must end in .gml.')
#    if re.search(r'[^A-Za-z\d_-]', file_name_array[0]):
#        raise argparse.ArgumentTypeError('File name must not contain non-alphanumeric characters.')
#    return str

def get_parser():
    """ Returns a custom argparse parser made for graph.py """
    parser = argparse.ArgumentParser(description='Reads the attributes of the nodes and edges in the file. Additional flags allow for additional visualization and more verbose output explaining per-round behavior of bipartite graphs.', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("graph_file", help="Path to the input graph file in .gml format.")

    parser.add_argument("--plot", action="store_true", help="Requests that the graph be plotted. This parameter triggers the visualization of the graph, which can include plotting nodes, edges, and possibly additional metrics or shortest path highlights.")
    
    parser.add_argument("--interactive", action="store_true", help="""Requests that the program show the output of every round graph. A round is defined as obtaining the preference
seller graph, compute the constricted sets via matching, and update the valuation.""")

    return parser
