import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def create_graph(csv_file):
    adj_df = pd.read_csv(csv_file, index_col=0)
    
    # Create a graph from the adjacency matrix
    G = nx.from_pandas_adjacency(adj_df)

    return G

csv_file_path = "outputs/adjacency_matrix.csv"  # Replace with your file
G = create_graph(csv_file_path)

def plot_degree_dist(G):
    degrees = [d for _, d in G.degree()]
    
    plt.figure(figsize=(12, 6))

    # Regular binning
    plt.subplot(1, 2, 1)
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2), edgecolor='black', align='left')
    plt.title("Degree Distribution (Regular Binning)")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")

    # Log binning
    plt.subplot(1, 2, 2)

    # Filter out zero degrees for log scaling
    non_zero_degrees = [d for d in degrees if d > 0]

    # Create log-spaced bins
    log_bins = np.logspace(np.log10(min(non_zero_degrees)), np.log10(max(non_zero_degrees)), num=20)
    plt.hist(non_zero_degrees, bins=log_bins, edgecolor='black')

    # Set log scale on axes
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Degree Distribution (Log Binning)")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("Frequency (log scale)")

    plt.tight_layout()
    plt.show()

plot_degree_dist(G)



