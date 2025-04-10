import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# 1. Create or load a graph (for demo, we use a random graph)
csv_file_path = "outputs/adjacency_matrix.csv"
adj_df = pd.read_csv(csv_file_path, index_col=0)
# Create a graph from the adjacency matrix
G = nx.from_pandas_adjacency(adj_df)

# 1. Degree Assortativity Coefficient
assortativity = nx.degree_pearson_correlation_coefficient(G)
print(f"Degree Assortativity (Pearson correlation coefficient): {assortativity:.4f}")

# 2. Average Neighbor Degree vs. Node Degree
degree = dict(G.degree())
avg_neighbor_deg = nx.average_neighbor_degree(G)

# Group by degree and compute mean of neighbor degrees for each degree value
deg_values = sorted(set(degree.values()))
avg_neighbor_by_deg = []
for k in deg_values:
    nodes_with_k = [n for n in G.nodes() if degree[n] == k]
    if nodes_with_k:
        mean_neighbor_deg = np.mean([avg_neighbor_deg[n] for n in nodes_with_k])
        avg_neighbor_by_deg.append(mean_neighbor_deg)
    else:
        avg_neighbor_by_deg.append(0)

# Plot average neighbor degree vs. node degree
plt.figure(figsize=(8, 6))
plt.scatter(deg_values, avg_neighbor_by_deg, marker='o')
plt.xlabel("Node Degree (k)")
plt.ylabel("Average Neighbor Degree (knn(k))")
plt.title("Average Neighbor Degree vs. Node Degree")
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Interpretation
if assortativity > 0.1:
    print("Interpretation: The network is assortative (high-degree nodes tend to connect to other high-degree nodes).")
elif assortativity < -0.1:
    print("Interpretation: The network is disassortative (high-degree nodes tend to connect to low-degree nodes).")
else:
    print("Interpretation: The network is neutral (no strong preference in degree correlation).")
