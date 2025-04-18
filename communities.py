import networkx as nx
from community import community_louvain # this is from python-louvain package
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
    # 1. Create or load a graph (for demo, we use a random graph)
    csv_file_path = "outputs/adjacency_matrix_filtered.csv"
    adj_df = pd.read_csv(csv_file_path, index_col=0)
    # Create a graph from the adjacency matrix
    G = nx.from_pandas_adjacency(adj_df)

    # 2. Detect communities using Louvain algorithm
    partition = community_louvain.best_partition(G)

    # 3. Number of communities
    num_communities = len(set(partition.values()))
    print(f"Number of communities: {num_communities}")

    # 5. Compute modularity score
    modularity = community_louvain.modularity(partition, G)
    print(f"Modularity score: {modularity:.4f}")


    # Count nodes in each community
    community_sizes = Counter(partition.values())
    print("Community sizes:")
    for community_id, size in community_sizes.items():
        print(f"Community {community_id}: {size} nodes")


