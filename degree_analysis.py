import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

def create_graph(csv_file):
    adj_df = pd.read_csv(csv_file, index_col=0)
    G = nx.from_pandas_adjacency(adj_df)
    return G

def estimate_power_law_gamma(degrees, k_min=1):
    """Estimate gamma using Maximum Likelihood Estimation for degrees > k_min"""
    degrees = np.array(degrees)
    degrees = degrees[degrees >= k_min]
    
    if len(degrees) == 0:
        raise ValueError("No degrees ≥ k_min")
    
    # MLE estimation of gamma
    gamma = 1 + len(degrees) / np.sum(np.log(degrees / (k_min - 0.5)))
    return gamma

def plot_degree_dist(G):
    # Compute degrees
    degrees = np.array([d for _, d in G.degree() if d > 0])

    print("Number of nodes =", G.number_of_nodes())
    print("Number of edges =", G.number_of_edges())
    print("Average degree = ", sum([d for (n, d) in nx.degree(G)]) / float(G.number_of_nodes()))
    # --------- Logarithmic binning ---------
    min_deg = min(degrees)
    max_deg = max(degrees)
    print("kmin = ", min_deg)
    print("kmax = ",max_deg)
    log_bins = np.logspace(np.log10(min_deg), np.log10(max_deg), num=20)
    hist, bin_edges = np.histogram(degrees, bins=log_bins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Estimate power-law gamma
    k_min = 78  # You can tweak this
    gamma = estimate_power_law_gamma(degrees, k_min)

    # Regular histogram
    plt.figure(figsize=(8, 6))
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2), align='left')
    plt.title("Degree Distribution (Regular Binning)")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")

    # Log-binned histogram + gamma
    plt.figure(figsize=(8, 6))
    plt.bar(bin_centers, hist, width=np.diff(bin_edges), align='center', edgecolor='black', alpha=0.7, label="Log-binned Histogram")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Degree (log scale)")
    plt.ylabel("P(Degree) (log scale)")
    plt.title(f"Degree Distribution (Log-Binned)\nEstimated γ ≈ {gamma:.2f}")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    csv_file_path = "adj/timeframe_2019_cleaned.csv"
    G = create_graph(csv_file_path)
    
    plot_degree_dist(G)
