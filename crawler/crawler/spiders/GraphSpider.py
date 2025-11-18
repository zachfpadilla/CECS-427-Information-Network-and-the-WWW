from pathlib import Path

from urllib.parse import urlparse
import scrapy
import networkx as nx

class GraphSpider(scrapy.Spider):
    name = "graph"

    def __init__(self, max_pages, domain, start_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.max_pages = int(max_pages) if max_pages else 100 # fallback just in case
        self.pages_visited = 0

        if domain is None:
            raise ValueError("domain must be non-empty")
        self.allowed_domains = [domain]

        
        if start_urls is None:
            self.start_urls = [domain]
        elif isinstance(start_urls, str):
            # split CLI argument into list
            self.start_urls = start_urls.split(",")
        else:
            self.start_urls = start_urls
        
        self.graph = nx.DiGraph()

    def parse(self, response):
        self.pages_visited += 1
        if self.pages_visited > self.max_pages:
            raise scrapy.exceptions.CloseSpider(f"Reached max pages: {self.max_pages}")
    
        for link in response.css("a::attr(href)").getall():
            url = response.urljoin(link)
            parsed = urlparse(url)
            if parsed.netloc in self.allowed_domains and parsed.path.startswith("/pid"):
                yield response.follow(link, callback=self.parse)

    def closed(self, reason):
        nx.write_gml(self.graph, "test.gml")
        self.logger.info(f"Graph saved to test.gml, reason: {reason}")
