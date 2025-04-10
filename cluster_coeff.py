import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1. Create or load a graph (for demo, we use a random graph)
csv_file_path = "outputs/adjacency_matrix.csv"
adj_df = pd.read_csv(csv_file_path, index_col=0)
# Create a graph from the adjacency matrix
G = nx.from_pandas_adjacency(adj_df)

# Step 1: Global Clustering Coefficient (Transitivity)
global_clustering = nx.transitivity(G)
print(f"🔵 Global Clustering Coefficient (Transitivity): {global_clustering:.4f}")

# Step 2: Compare to Random Graph (same number of nodes and edges)
n_nodes = G.number_of_nodes()
n_edges = G.number_of_edges()
p_edge = (2 * n_edges) / (n_nodes * (n_nodes - 1))  # approximate edge probability

G_random = nx.gnp_random_graph(n=n_nodes, p=p_edge, seed=42)
random_clustering = nx.transitivity(G_random)
print(f"🟣 Random Graph Clustering Coefficient: {random_clustering:.4f}")

# Step 3: Local Clustering Coefficients
local_clustering = nx.clustering(G)

# Step 4: Top 10 nodes by degree
top_degree_nodes = sorted(G.degree(), key=lambda x: x[1], reverse=True)[:10]
top_nodes = [node for node, _ in top_degree_nodes]

# Create a table
clustering_data = {
    "Node": top_nodes,
    "Degree": [G.degree(n) for n in top_nodes],
    "Local Clustering Coef": [local_clustering[n] for n in top_nodes]
}

df_clustering = pd.DataFrame(clustering_data)
print("\n📊 Top 10 Nodes by Degree - Clustering Coefficients:")
print(df_clustering)

# Step 5 (Optional): Plot
plt.figure(figsize=(10, 5))
plt.bar(df_clustering["Node"], df_clustering["Local Clustering Coef"], color="skyblue")
plt.title("Local Clustering Coefficients (Top 10 Nodes by Degree)")
plt.xlabel("Node")
plt.ylabel("Clustering Coefficient")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
