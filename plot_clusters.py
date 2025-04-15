import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import Counter
import pandas as pd
import numpy as np

# Load graph from adjacency matrix
adj_file = "outputs/adjacency_matrix_filtered.csv"
corr_file = "outputs/correlation_matrix_filtered.csv"

# Load adjacency and correlation matrices
adj_df = pd.read_csv(adj_file, index_col=0)
corr_df = pd.read_csv(corr_file, index_col=0)
corr_df = corr_df.loc[adj_df.index, adj_df.columns]  # Ensure alignment

# Build full graph with weights = 1 - |correlation| (used as distances)
distance_df = 1 - corr_df.abs()
np.fill_diagonal(distance_df.values, 0)
G_full = nx.from_pandas_adjacency(distance_df)

# Generate MST for layout
mst = nx.minimum_spanning_tree(G_full, weight='weight')

# Louvain community detection on the original (adjacency-based) graph
G = nx.from_pandas_adjacency(adj_df)
partition = community_louvain.best_partition(G)

# Top 4 communities
comm_counter = Counter(partition.values())
top_4_communities = [c for c, _ in comm_counter.most_common(4)]

# Assign colors
color_palette = ['red', 'blue', 'green', 'orange']
color_map = {comm_id: color_palette[i] for i, comm_id in enumerate(top_4_communities)}
default_color = 'lightgray'

# Assign node colors
node_colors = [
    color_map[partition[n]] if partition[n] in top_4_communities else default_color
    for n in G.nodes()
]

# Use MST layout (spring layout on MST for structure)
pos = nx.spring_layout(mst, seed=42)

# Draw full graph using MST layout
plt.figure(figsize=(20, 12))
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100, alpha=0.9)
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), alpha=0.05, width=0.3)
nx.draw_networkx_labels(G, pos, font_size=6)

plt.title("Top 4 Louvain Communities with MST-Based Layout", fontsize=16)
plt.axis('off')
plt.tight_layout()
plt.show()
