import networkx as nx
import matplotlib.pyplot as plt

# Delivery zones
zones = ["A", "B", "C", "D"]

# Weighted connections
edges = [
    ("A", "B", 5),
    ("A", "C", 2),
    ("A", "D", 4),
    ("B", "C", 3),
    ("B", "D", 6),
    ("C", "D", 1)
]

# Optimal partition found by classical Max-Cut
group_1 = ["A", "B"]
group_2 = ["C", "D"]

# Create graph
G = nx.Graph()
G.add_nodes_from(zones)

for u, v, weight in edges:
    G.add_edge(u, v, weight=weight)

# Draw graph
pos = {
    "A": (-1, 1),
    "B": (1, 1),
    "C": (-1, -1),
    "D": (1, -1)
}

colors = [
    "skyblue" if node in group_1 else "orange"
    for node in G.nodes()
]

plt.figure(figsize=(9, 6))

nx.draw_networkx_nodes(
    G, pos,
    node_color=colors,
    node_size=1800
)

nx.draw_networkx_labels(
    G, pos,
    font_size=16,
    font_weight="bold"
)

nx.draw_networkx_edges(
    G, pos,
    width=2
)

edge_labels = nx.get_edge_attributes(G, "weight")

nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=12
)

plt.title("Delivery Zone Partitioning - Max-Cut")
plt.figtext(
    0.5, 0.02,
    "Blue: Group 1 | Orange: Group 2 | Maximum Cut = 15",
    ha="center",
    fontsize=11
)

plt.axis("off")
plt.tight_layout()
plt.show()
