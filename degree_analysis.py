import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
# import powerlaw

def create_graph(csv_file):
    adj_df = pd.read_csv(csv_file, index_col=0)
    
    # Create a graph from the adjacency matrix
    G = nx.from_pandas_adjacency(adj_df)

    return G

csv_file_path = "outputs/adjacency_matrix.csv"  # Replace with your file

G = create_graph(csv_file_path)

print("Number of nodes = ", G.number_of_nodes())
print("Number of edges = ", G.number_of_edges())

def plot_degree_dist(G):
    # Compute degree for each node
    degrees = [d for _, d in G.degree()]
    degrees = np.array([d for d in degrees if d > 0])

    # --------- Logarithmic binning ---------
    min_deg = min(degrees)
    max_deg = max(degrees)

    # Create logarithmic bins
    log_bins = np.logspace(np.log10(min_deg), np.log10(max_deg), num=20)
    hist, bin_edges = np.histogram(degrees, bins=log_bins, density=True)

    # Compute bin centers for plotting
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Regular binning
    plt.figure(figsize=(8, 6))
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2), align='left')
    plt.title("Degree Distribution (Regular Binning)")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")

 
    # Plot histogram with log-log axes
    plt.figure(figsize=(8, 6))
    plt.bar(bin_centers, hist, width=np.diff(bin_edges), align='center', edgecolor='black', alpha=0.7, label="Log-binned Histogram")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("P(Degree) (log scale)")
    plt.title("Degree Distribution (Log-Binned Histogram)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)


    plt.legend()
    plt.tight_layout()
    plt.show()

plot_degree_dist(G)



