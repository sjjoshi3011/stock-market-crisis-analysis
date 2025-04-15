import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Print results
def print_top(metric_name, top_list):
    print(f"\nTop nodes by {metric_name}:")
    for node, score in top_list:
        print(f"Node {node}: {score:.4f}")


def get_top_nodes_by_centrality(G):
    top_nodes = {}

    # Closeness
    closeness = nx.closeness_centrality(G)
    top_nodes['Closeness'] = sorted(closeness, key=closeness.get, reverse=True)[:3]

    # Betweenness
    betweenness = nx.betweenness_centrality(G)
    top_nodes['Betweenness'] = sorted(betweenness, key=betweenness.get, reverse=True)[:3]

    # Eigenvector
    try:
        eigen = nx.eigenvector_centrality(G, max_iter=1000)
        top_nodes['Eigenvector'] = sorted(eigen, key=eigen.get, reverse=True)[:3]
    except nx.PowerIterationFailedConvergence:
        top_nodes['Eigenvector'] = ["Convergence failed"]

    # HITS
    hits_hubs, hits_authorities = nx.hits(G, max_iter=1000)
    top_nodes['HITS_Hub'] = sorted(hits_hubs, key=hits_hubs.get, reverse=True)[:3]
    top_nodes['HITS_Authority'] = sorted(hits_authorities, key=hits_authorities.get, reverse=True)[:3]

    return top_nodes


def print_centralities(csv_file_path):
    adj_df = pd.read_csv(csv_file_path, index_col=0)
    # Create a graph from the adjacency matrix
    G = nx.from_pandas_adjacency(adj_df)

    # Eigenvector Centrality
    eigen_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    top_eigen = sorted(eigen_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    print_top("Eigenvector Centrality", top_eigen)

    # Katz Centrality
    # katz_centrality = nx.katz_centrality(G, alpha=0.005, beta=1.0, max_iter=5000)
    # top_katz = sorted(katz_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    # print_top("Katz Centrality", top_katz)


    # Betweenness Centrality
    betweenness_centrality = nx.betweenness_centrality(G)
    top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    print_top("Betweenness Centrality", top_betweenness)

    # Closeness Centrality
    closeness_centrality = nx.closeness_centrality(G)
    top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    print_top("Closeness Centrality", top_closeness)

    # HITS (Authority and Hub Scores)
    hits_hubs, hits_auth = nx.hits(G, max_iter=1000)
    top_hubs = sorted(hits_hubs.items(), key=lambda x: x[1], reverse=True)[:10]
    top_auths = sorted(hits_auth.items(), key=lambda x: x[1], reverse=True)[:10]
    print_top("HITS - Hub Scores", top_hubs)
    print_top("HITS - Authority Scores", top_auths)

if __name__ == '__main__':
    csv_file_path = "outputs/adjacency_matrix.csv"
    print_centralities(csv_file_path)


