import networkx as nx
from community import community_louvain  # from python-louvain package
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import numpy as np


def community_detection(G):
    partition = community_louvain.best_partition(G)
    modularity = community_louvain.modularity(partition, G)
    num_communities = len(set(partition.values()))
    return partition, modularity, num_communities

if __name__ == '__main__':
    # 1. Load the graph from CSV adjacency matrix
    csv_file_path = "outputs/adjacency_matrix_filtered.csv"
    adj_df = pd.read_csv(csv_file_path, index_col=0)
    G = nx.from_pandas_adjacency(adj_df)

    # 2. Louvain community detection
    partition = community_louvain.best_partition(G)

    # 3. Count and print number of communities
    num_communities = len(set(partition.values()))
    print(f"Number of communities: {num_communities}")

    # 4. Compute modularity
    modularity = community_louvain.modularity(partition, G)
    print(f"Modularity score: {modularity:.4f}")

    # 5. Count nodes per community
    community_sizes = Counter(partition.values())
    print("Community sizes:")
    for community_id, size in community_sizes.items():
        print(f"Community {community_id}: {size} nodes")

    # 6. Prepare data for pie chart
    grouped_sizes = {}
    others_count = 0
    for comm_id, size in community_sizes.items():
        if size == 1:
            others_count += 1
        else:
            grouped_sizes[f'Community {comm_id}'] = size
    if others_count > 0:
        grouped_sizes["Others"] = others_count

    # Pie chart
    labels = list(grouped_sizes.keys())
    sizes = list(grouped_sizes.values())

    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(
        sizes,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        textprops={'fontsize': 10}
    )

    plt.title("Community Distribution (Louvain)", fontsize=14)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()
