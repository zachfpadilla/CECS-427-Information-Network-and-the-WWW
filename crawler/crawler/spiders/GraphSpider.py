from pathlib import Path
from urllib.parse import urlparse
import scrapy
import networkx as nx

class GraphSpider(scrapy.Spider):
    name = "graph"

    custom_settings = {
        "SPIDER_MIDDLEWARES": {
            "crawler.crawler.middlewares.EdgeCollectorMiddleware": 543,
        }
    }

    def __init__(self, domain, start_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # parse domain
        parsed = urlparse(domain)
        self.allowed_domains = [parsed.netloc or domain.replace("https://", "").replace("http://", "")]
        self.allowed_path_prefix = parsed.path if parsed.path else ""
        self.pages_visited = 0
        # parse start URLs
        if isinstance(start_urls, str):
            self.start_urls = start_urls.split(",")
        else:
            self.start_urls = start_urls

            self.pages_visited = len(self.start_urls)
        

        # graph + visited set
        self.graph = nx.DiGraph()

    def parse(self, response):
        url = response.url

        self.pages_visited += 1

        if self.pages_visited > 10: # limit crawler. will always have more than 100 nodes by 100 individual pages visited
            raise scrapy.exceptions.CloseSpider(f"Reached max pages: {self.max_pages}")

        # Follow allowed links
        for href in response.css("a::attr(href)").getall():
            target = response.urljoin(href)
            p = urlparse(target)

            if p.netloc == self.allowed_domains[0] and p.path.startswith(self.allowed_path_prefix):
                yield scrapy.Request(target, callback=self.parse)

    def closed(self, reason):
        nx.write_gml(self.graph, "test.gml")
        self.logger.info(f"Saved graph with {self.graph.number_of_nodes()} nodes")

