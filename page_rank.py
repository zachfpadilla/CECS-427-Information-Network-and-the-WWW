import networkx as nx
from cli import get_parser
from visualization import visualize_graph
from scrapy.crawler import CrawlerProcess
from crawler.crawler.spiders import GraphSpider
from urllib.parse import urlparse
import matplotlib.pyplot as plt
from scrapy import signals
from scrapy.signalmanager import dispatcher

spider_ref = {}

def spider_closed(spider, reason):
    spider_ref["instance"] = spider

def is_valid_url(url: str) -> bool:
    """
    Returns True if the URL has a valid format (scheme + netloc).
    """
    try:
        parsed = urlparse(url)
        # Must have scheme (http, https) and network location
        return all([parsed.scheme in ("http", "https"), parsed.netloc])
    except Exception:
        return False

def is_valid_domain(domain):
    # Add scheme if missing for parsing
    if "://" not in domain:
        domain = "http://" + domain
    parsed = urlparse(domain)
    return bool(parsed.netloc)

def normalize_domain(domain: str):
    """
    Takes a domain string and returns a tuple (netloc, path).
    Fixes missing scheme or leading/trailing slashes.
    """
    # Add scheme if missing (urlparse needs it to correctly extract netloc)
    if "://" not in domain:
        domain = "http://" + domain  # temporary scheme for parsing

    parsed = urlparse(domain)
    netloc = parsed.netloc.strip().lower()  # normalize netloc
    path = parsed.path or "/"              # default path to "/"

    # Ensure path starts with a single slash
    if not path.startswith("/"):
        path = "/" + path

    # Remove trailing slash (optional, depends on your use case)
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    return netloc, path

parser = get_parser()
args = parser.parse_args()

if args.crawler_graph and not args.crawler:
    parser.error("--crawler_graph requires --crawler")

if args.pagerank_values and not (args.crawler or args.input):
    parser.error("--pagerank_values requires --crawler or --input")

G = None

if args.input:
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

if args.crawler:
    try:
        #read file
        with open(args.crawler, "r", encoding="utf-8") as f:
            lines = f.readlines()  # list of strings

        #invalid format
        if len(lines) < 3:
            raise Exception("File not at least 3 lines long")

        #line 1 wrong
        max_nodes = lines[0]
        try:
            max_nodes = int(max_nodes)
        except ValueError: 
            raise ValueError(f"line 0 must be an integer representing max_nodes.")
            
        # line 2 wrong
        domain = lines[1].strip()
        if not is_valid_domain(domain):
            raise Exception("domain not a valid url")

        # format domain and path for spider
        netloc, path = normalize_domain(domain)
        
        #lines 3-? wrong
        start_urls = [line.strip() for line in lines[2:]]
        valid_urls = all(is_valid_url(url) for url in start_urls)
        if not valid_urls:
            raise Exception("not all urls are a valid format")

        print(lines[:5])  # first 5 lines

        process = CrawlerProcess()
        
        # Pass the spider class and kwargs
        process.crawl(GraphSpider, domain=netloc+path, start_urls=start_urls)
        
        # Connect the signal BEFORE starting
        dispatcher.connect(spider_closed, signal=signals.spider_closed)
        
        # Start crawling (blocking)
        process.start()
        
        # Retrieve the actual spider instance
        spider = spider_ref.get("instance")
        G = spider.graph        # only 100 nodes graph

        nodes_with_id = [(n, int(attrs.get("id", 0))) for n, attrs in G.nodes(data=True)]
        nodes_with_id.sort(key=lambda x: x[1])
        filtered_nodes = [n for n, _ in nodes_with_id[:max_nodes]]

        G = G.subgraph(filtered_nodes).copy()

        plt.figure(figsize=(12, 8))
        pos = nx.kamada_kawai_layout(G)  # usually faster for dense graphs than spring_layout
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", edge_color="gray")
        plt.show()

    except Exception as e:
        print(f"Caught exception: {e}")

if args.loglogplot:
    pass
    #print("\nGenerating plot...")
    #visualize_graph(G)

if args.crawler_graph:
    nx.write_gml(G, args.crawler_graph)

if args.pagerank_values:
    pass
