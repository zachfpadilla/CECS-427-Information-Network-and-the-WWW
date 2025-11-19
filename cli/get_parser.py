import argparse

def gml_file(file_path):
    if not file_path.endswith('.gml'):
        raise argparse.ArgumentTypeError(f"File '{file_path}' is not a .gml file.")
    return file_path

def get_parser():
    """ Returns a custom argparse parser made for graph.py """
    parser = argparse.ArgumentParser(description='Reads the attributes of the nodes and edges in the file. Additional flags allow for additional visualization and more verbose output explaining per-round behavior of bipartite graphs.', formatter_class=argparse.RawTextHelpFormatter)

    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument("--crawler", type=str, help="Generate a graph by crawling the internet starting with the addresses listed in the text file.")
    input_group.add_argument("--input", type=gml_file, help="Uses a gml file as input for the PageRank algorithm and to plot the loglog plot.")


    parser.add_argument("--loglogplot", action="store_true", help="Plots the loglogplot based on the input.")
    
    parser.add_argument("--crawler_graph", type=gml_file, help="Exports the graph to a .gml file.")

    parser.add_argument("--pagerank_values", type=str, help="Exports the pagerank values to a txt file.")
    return parser
