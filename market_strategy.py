import networkx as nx
from cli import get_parser
from visualization import visualize_graph
from verification import verify_bipartite_graph
from interactive_logic import *

parser = get_parser()
args = parser.parse_args()

G = None

try:
    G = nx.read_gml(args.graph_file)
    print(f"Successfully loaded graph from '{args.graph_file}'.")
    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
except FileNotFoundError:
    print(f"Error: The file '{args.graph_file}' was not found.")
    exit(1)
except Exception as e:
    print(f"Error: Failed to parse GML file. Reason: {e}")
    exit(1)

if not verify_bipartite_graph(G):
    print(f"Error: The GML file does not contain a valid bipartite graph.")
    exit(1)


print("\n--- Initial State ---")
sellers, buyers = nx.bipartite.sets(G)


def get_node_label(graph, node_id):
    return graph.nodes[node_id].get('label', node_id)


print("Seller Prices:")
for node in sellers:
    price = G.nodes[node].get('price', 'N/A')
    print(f"  {get_node_label(G, node)}: {price}")

round_num = 1
while True:
    if args.interactive:
        print(f"\n----- Round {round_num} -----")

    #obtain the preference graph based on current prices
    preferred_graph = get_preferred_seller_graph(G, sellers, buyers)

    #compute constricted sets via matching
    constricted_buyers, neighbor_sellers = find_constricted_set(preferred_graph, buyers, sellers)

    #check if the market has cleared
    if not constricted_buyers:
        print("\nMarket cleared; a perfect matching is possible at current prices.")
        final_matching = nx.bipartite.maximum_matching(preferred_graph, top_nodes=buyers)
        print("Final Matching (Buyer: Seller):")
        for buyer, seller in final_matching.items():
            print(f"  {get_node_label(G, buyer)} -> {get_node_label(G, seller)}")
        break

    #if not cleared, update prices and report
    if args.interactive:
        constricted_labels = {get_node_label(G, b) for b in constricted_buyers}
        neighbor_labels = {get_node_label(G, s) for s in neighbor_sellers}
        print(f"Found constricted set of buyers: {constricted_labels}")
        print(f"Their preferred neighborhood of sellers: {neighbor_labels}")
        print("Increasing prices for sellers in the neighborhood...")

    update_prices(G, neighbor_sellers)

    #plot each round's preference graph
    if args.interactive:
        print("New Seller Prices:")
        for node in sellers:
            price = G.nodes[node].get('price', 'N/A')
            print(f"  {get_node_label(G, node)}: {price}")

    round_num += 1
    if round_num > 100:  #arbitrary number
        print("Algorithm ran for too long. Halting.")
        break

if args.plot:
    print("\nGenerating plot...")
    visualize_graph(preferred_graph, matching=final_matching)