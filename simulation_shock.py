import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from plot_graph import create_graph_from_adjacency
from centralities import get_top_nodes_by_centrality
from shockwave import build_graph_from_correlation_csv, simulate_shock_propagation, summarize_shock_effects



def simulate_shocks_from_top_central_nodes(G, top_nodes, initial_shock=-0.05, steps=4, decay=0.2):

    for centrality_type, nodes in top_nodes.items():
        if nodes == ["Convergence failed"]:
            print(f"⚠️ Skipping {centrality_type} due to eigenvector convergence issue.")
            continue

        for i, seed_node in enumerate(nodes, start=1):
            print(f"\n🚨 Simulating shock from top {i} {centrality_type} node: {seed_node}")
            shocks = simulate_shock_propagation(G, seed_node, initial_shock=initial_shock, steps=steps, decay=decay)
            summarize_shock_effects(shocks)

def simulate_shocks_from_bottom_central_nodes(G, bottom_nodes, initial_shock=-0.05, steps=4, decay=0.2):
    for centrality_type, nodes in bottom_nodes.items():
        if nodes == ["Convergence failed"]:
            print(f"⚠️ Skipping {centrality_type} due to eigenvector convergence issue.")
            continue

        for i, seed_node in enumerate(nodes, start=1):
            print(f"\n🌊 Simulating shock from bottom {i} {centrality_type} node: {seed_node}")
            shocks = simulate_shock_propagation(G, seed_node, initial_shock=initial_shock, steps=steps, decay=decay)
            summarize_shock_effects(shocks)


if __name__ == '__main__':
    csv_file_path = "outputs/adjacency_matrix_filtered.csv"  
    corr_csv_file = "outputs/correlation_matrix_filtered.csv" 

    G = create_graph_from_adjacency(csv_file_path)
    top_nodes = get_top_nodes_by_centrality(G)

    G2 = build_graph_from_correlation_csv(corr_csv_file)
    simulate_shocks_from_top_central_nodes(G2,top_nodes)





