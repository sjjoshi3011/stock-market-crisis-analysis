import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_graph_from_adjacency(csv_file):
    # Load the adjacency matrix
    adj_df = pd.read_csv(csv_file, index_col=0)
    
    # Create a weighted graph (weights from adjacency)
    G = nx.from_pandas_adjacency(adj_df)
    
    return G

def plot_mst_graph(G):
    # Convert to a complete graph with edge weights
    # We'll treat original edges as weighted for MST calc
    # Invert weights: higher correlation → lower distance
    G_weighted = G.copy()
    for u, v in G_weighted.edges():
        G_weighted[u][v]['weight'] = 1.0 / (G_weighted[u][v].get('weight', 1) + 1e-6)

    # Get the Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G_weighted, weight='weight')

    # Compute layout from MST
    pos = nx.spring_layout(mst, seed=42, k=0.4, scale=3.0)

    # Node sizes based on raw degree
    degrees = dict(G.degree())
    node_sizes = [degrees[n] * 10 for n in G.nodes()]  # Scale factor can be adjusted

    # Draw graph using MST layout
    plt.figure(figsize=(18, 18))
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='skyblue', edgecolors='black')
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.6)
    # nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title('Graph Visualized with MST Layout (Node Size ~ Degree)', fontsize=14)
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    csv_file_path = "outputs/adjacency_matrix_filtered.csv"
    G = create_graph_from_adjacency(csv_file_path)
    plot_mst_graph(G)
