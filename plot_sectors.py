import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def create_mst_graph(csv_file, sector_file):
    # Load adjacency matrix (filtered)
    adj_df = pd.read_csv(csv_file, index_col=0)
    
    # Use correlation weights (inverse of adjacency: 1 if correlated > threshold, else 0)
    # We'll use the correlation values directly for MST (invert them for distance)
    corr_df = pd.read_csv("outputs/correlation_matrix_filtered.csv", index_col=0)
    corr_df = corr_df.loc[adj_df.index, adj_df.columns]  # Align indices

    # Convert to distance: 1 - |correlation|
    distance_df = 1 - corr_df.abs()
    np.fill_diagonal(distance_df.values, 0)  # Ensure diagonal is zero

    # Build full weighted graph
    G_full = nx.from_pandas_adjacency(distance_df)

    # Compute the Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G_full, weight='weight')

    # Load industry sector mapping
    sectors_df = pd.read_csv(sector_file)
    industry_map = dict(zip(sectors_df["Symbol"], sectors_df["Industry"]))

    # Assign industry as a node attribute
    for node in mst.nodes:
        industry = industry_map.get(node, "Unknown")
        mst.nodes[node]["industry"] = industry

    # Assign colors to industries
    industries = sorted(set(industry_map.values()))
    cmap = plt.get_cmap("tab20")
    color_list = [cmap(i) for i in range(len(industries))]
    color_map = dict(zip(industries, color_list))
    # Assign node colors based on industry
    node_colors = [
        color_map.get(mst.nodes[node]["industry"], "#333333")  # default gray
        for node in mst.nodes
    ]

    # Create legend
    handles = [plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor=color_map[ind], markersize=10, label=ind)
               for ind in industries]

    # Draw the MST
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(mst, seed=42)  # Consistent layout
    nx.draw_networkx(
        mst,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=600,
        edge_color='gray',
        font_size=8
    )

    # Create legend
    handles = [plt.Line2D([0], [0], marker='o', color='w',
               markerfacecolor=color_map[ind], markersize=10, label=ind)
               for ind in industries]
    plt.legend(handles=handles, title="Industry", loc='upper left', bbox_to_anchor=(1, 1))
    plt.title('Minimum Spanning Tree Colored by Industry')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    csv_file_path = "outputs/adjacency_matrix_filtered.csv"
    sector_file_path = "outputs/combined_sectors.csv"
    create_mst_graph(csv_file_path, sector_file_path)
