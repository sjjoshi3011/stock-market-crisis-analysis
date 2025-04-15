import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def create_graph_from_adjacency(csv_file):
    # Load the adjacency matrix
    adj_df = pd.read_csv(csv_file, index_col=0)
    
    # Create a graph from the adjacency matrix
    G = nx.from_pandas_adjacency(adj_df)
    
    # Draw the graph
    plt.figure(figsize=(10, 10))
    nx.draw(G, with_labels=True, node_size=500, node_color='lightblue', edge_color='gray')
    plt.title('Graph from Adjacency Matrix')
    plt.show()


if __name__ == '__main__':
    # Example usage
    csv_file_path = "outputs/adjacency_matrix_filtered.csv"  # Replace with your file
    create_graph_from_adjacency(csv_file_path)
