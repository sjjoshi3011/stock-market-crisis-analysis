import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import Counter
import matplotlib.patches as mpatches
import numpy as np
from sklearn.metrics import normalized_mutual_info_score

# Load adjacency and sector files
adj_file = "outputs/adjacency_matrix_filtered.csv"
sector_file = "outputs/combined_sectors.csv"
corr_file = "outputs/correlation_matrix_filtered.csv"

# Load data
adj_df = pd.read_csv(adj_file, index_col=0)
corr_df = pd.read_csv(corr_file, index_col=0)
G = nx.from_pandas_adjacency(adj_df)

# Load sector info and map
sector_df = pd.read_csv(sector_file)
sector_df = sector_df[sector_df["Symbol"].isin(G.nodes())]
sector_map = dict(zip(sector_df["Symbol"], sector_df["Industry"]))
industry_labels = [sector_map.get(node, "Unknown") for node in G.nodes()]

# --- Community Detection using Louvain ---
partition = community_louvain.best_partition(G)
community_labels = [partition[node] for node in G.nodes()]
community_ids = sorted(set(community_labels))
community_sizes = Counter(community_labels)

# --- Filter Top N communities ---
N = 6
top_communities = [c for c, _ in community_sizes.most_common(N)]
filtered_nodes = [node for node in G.nodes() if partition[node] in top_communities]
G_sub = G.subgraph(filtered_nodes)

# Recompute layout (Spring and MST)
spring_pos = nx.spring_layout(G_sub, seed=42)

# MST-based layout
distance_df = 1 - corr_df.abs()
nodes = list(G_sub.nodes())
distance_df = distance_df.loc[nodes, nodes]
np.fill_diagonal(distance_df.values, 0)
G_dist = nx.from_pandas_adjacency(distance_df)
mst = nx.minimum_spanning_tree(G_dist, weight='weight')
mst_pos = nx.spring_layout(mst, seed=42)

# Colors for communities
cmap = plt.get_cmap('tab10')
color_map = {c: cmap(i % 10) for i, c in enumerate(top_communities)}
node_colors = [color_map[partition[n]] for n in G_sub.nodes()]

# --- Plot 1: Spring Layout ---
plt.figure(figsize=(12, 8))
nx.draw_networkx_edges(G_sub, spring_pos, alpha=0.1, width=0.5)
nx.draw_networkx_nodes(G_sub, spring_pos, node_color=node_colors, node_size=80, alpha=0.95)
plt.title(f"Louvain Communities (Top {N}) - Spring Layout")
plt.axis('off')
plt.tight_layout()
plt.show()

# --- Plot 2: MST Layout ---
plt.figure(figsize=(12, 8))
nx.draw_networkx_edges(G_sub, mst_pos, alpha=0.1, width=0.5)
nx.draw_networkx_nodes(G_sub, mst_pos, node_color=node_colors, node_size=80, alpha=0.95)
plt.title(f"Louvain Communities (Top {N}) - MST-Based Layout")
plt.axis('off')
plt.tight_layout()
plt.show()

# --- Quantitative Comparison ---
# Align lists
common_nodes = list(G.nodes())
predicted = [partition[node] for node in common_nodes]
actual = [sector_map.get(node, "Unknown") for node in common_nodes]

# Compute NMI
nmi_score = normalized_mutual_info_score(actual, predicted)

print(nmi_score)

