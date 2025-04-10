import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import defaultdict, Counter
import pandas as pd

# 1. Create or load a graph (for demo, we use a random graph)
csv_file_path = "outputs/adjacency_matrix.csv"
adj_df = pd.read_csv(csv_file_path, index_col=0)
# Create a graph from the adjacency matrix
G = nx.from_pandas_adjacency(adj_df)


# Step 1: Louvain partitioning
partition = community_louvain.best_partition(G)

# Step 2: Count sizes of each community
comm_counter = Counter(partition.values())
top_4_communities = [c for c, _ in comm_counter.most_common(4)]

# Step 3: Assign distinct colors to top 4 communities
color_map = {
    top_4_communities[0]: 'red',
    top_4_communities[1]: 'blue',
    top_4_communities[2]: 'green',
    top_4_communities[3]: 'orange'
}
default_color = 'lightgray'

# Step 4: Positioning - layout that clusters by community
# Separate layout per community with shifting
pos = {}
for i, comm_id in enumerate(top_4_communities):
    nodes = [n for n in G.nodes() if partition[n] == comm_id]
    sub_pos = nx.spring_layout(G.subgraph(nodes), seed=42)
    shift_x, shift_y = (i % 2) * 5, (i // 2) * 5
    for node in sub_pos:
        pos[node] = (sub_pos[node][0] + shift_x, sub_pos[node][1] + shift_y)

# Add remaining nodes (other communities) to pos (optional)
for node in G.nodes():
    if node not in pos:
        pos[node] = (0, 0)  # collapsed in a corner

# Step 5: Assign colors
node_colors = [
    color_map[partition[n]] if partition[n] in top_4_communities else default_color
    for n in G.nodes()
]

# Step 6: Draw
plt.figure(figsize=(20, 12))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100)
nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.3)
nx.draw_networkx_labels(G, pos, font_size=6)

plt.title("Top 4 Louvain Communities by Size", fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.show()
