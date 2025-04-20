import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from collections import Counter
import numpy as np
from sklearn.metrics import normalized_mutual_info_score
from scipy.spatial import ConvexHull
from matplotlib.patches import Polygon

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
partition_sub = {node: partition[node] for node in G_sub.nodes()}

# Layouts
spring_pos = nx.spring_layout(G_sub, seed=42, k=0.5)

distance_df = 1 - corr_df.abs()
nodes = list(G_sub.nodes())
distance_df = distance_df.loc[nodes, nodes]
np.fill_diagonal(distance_df.values, 0)
G_dist = nx.from_pandas_adjacency(distance_df)
mst = nx.minimum_spanning_tree(G_dist, weight='weight')
mst_pos = nx.spring_layout(mst, seed=42, k=0.5)

# Colors for communities
cmap = plt.get_cmap('tab10')
color_map = {c: cmap(i % 10) for i, c in enumerate(top_communities)}
node_colors = [color_map[partition[n]] for n in G_sub.nodes()]

# Node sizes
degrees_sub = dict(G_sub.degree())
node_sizes = [degrees_sub[n] * 10 for n in G_sub.nodes()]

# --- Helper: Draw convex hulls around communities ---
def draw_community_hulls(ax, pos, partition, color_map, alpha=0.2):
    from collections import defaultdict
    grouped = defaultdict(list)
    for node, comm in partition.items():
        grouped[comm].append(node)

    for comm_id, members in grouped.items():
        if len(members) < 3:
            continue  # Need 3 points for a polygon
        pts = np.array([pos[n] for n in members])
        hull = ConvexHull(pts)
        polygon = Polygon(pts[hull.vertices], alpha=alpha, facecolor=color_map.get(comm_id, "gray"), linewidth=0)
        ax.add_patch(polygon)

# --- Plot 1: Spring Layout with Shaded Communities ---
fig, ax = plt.subplots(figsize=(14, 10))
nx.draw_networkx_edges(G_sub, spring_pos, ax=ax, alpha=0.3, width=0.5)
draw_community_hulls(ax, spring_pos, partition_sub, color_map)
nx.draw_networkx_nodes(G_sub, spring_pos, ax=ax, node_size=node_sizes, node_color=node_colors, alpha=0.95)
nx.draw_networkx_labels(G_sub, spring_pos, ax=ax, font_size=7)
plt.title(f"Louvain Communities (Top {N}) - Spring Layout with Shading")
plt.axis('off')
plt.tight_layout()
plt.show()

# --- Plot 2: MST Layout ---
plt.figure(figsize=(12, 8))
nx.draw_networkx_edges(G_sub, mst_pos, alpha=0.3, width=0.5)
nx.draw_networkx_nodes(G_sub, mst_pos, node_color=node_colors, node_size=80, alpha=0.95)
plt.title(f"Louvain Communities (Top {N}) - MST-Based Layout")
plt.axis('off')
plt.tight_layout()
plt.show()

# --- Quantitative Comparison ---
common_nodes = [n for n in G.nodes() if n in sector_map]
predicted = [partition[n] for n in common_nodes]
actual = [sector_map[n] for n in common_nodes]

nmi_score = normalized_mutual_info_score(actual, predicted)
print(f"NMI Score between Louvain communities and industry sectors: {nmi_score:.4f}")
