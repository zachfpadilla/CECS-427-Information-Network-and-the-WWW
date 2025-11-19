
import networkx as nx
import matplotlib.pyplot as plt

# 1️⃣ Read the GML file
G = nx.read_gml("test.gml")

# 2️⃣ Sort nodes by their 'id' attribute (convert to int) and take the first 100
nodes_with_id = [(n, int(attrs.get("id", 0))) for n, attrs in G.nodes(data=True)]
nodes_with_id.sort(key=lambda x: x[1])
filtered_nodes = [n for n, _ in nodes_with_id[:100]]

# 3️⃣ Create subgraph
H = G.subgraph(filtered_nodes).copy()

# 4️⃣ Plot using a faster layout for large graphs
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(H)  # usually faster for dense graphs than spring_layout
nx.draw(H, pos, with_labels=True, node_size=500, node_color="skyblue", edge_color="gray")
plt.show()

