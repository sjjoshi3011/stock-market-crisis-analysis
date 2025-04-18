import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

def build_graph_from_correlation_csv(csv_path, threshold=0.3):
    # Read CSV and convert to DataFrame
    df = pd.read_csv(csv_path, index_col=0)

    # Initialize undirected graph
    G = nx.Graph()

    for i in df.index:
        for j in df.columns:
            if i != j:
                weight = df.loc[i, j]
                if abs(weight) >= threshold:
                    G.add_edge(i, j, weight=weight)
    
    return G

def simulate_shock_propagation(G, seed_node, initial_shock=-0.05, steps=4, decay=0.5):
    shock = {node: 0.0 for node in G.nodes}
    shock[seed_node] = initial_shock

    shocks_over_time = [shock.copy()]
    
    for _ in range(steps):
        new_shock = shock.copy()
        for node in G.nodes:
            influence = 0.0
            for neighbor in G.neighbors(node):
                weight = G[node][neighbor]['weight']
                influence += shock[neighbor] * weight
            new_shock[node] += decay * influence
        shock = new_shock
        shocks_over_time.append(shock.copy())
    
    return shocks_over_time

def print_shock_results(shocks_over_time):
    print("Time Step | Node -> Shock Value")
    for t, shock_dict in enumerate(shocks_over_time):
        print(f"\nTime {t}")
        for node, val in shock_dict.items():
            print(f"{node}: {val:.4f}")

def summarize_shock_effects(shocks_over_time):
    final_shock = shocks_over_time[-1]

    fallen = [stock for stock, value in final_shock.items() if value < 0]
    risen = [stock for stock, value in final_shock.items() if value > 0]
    total_shock = sum(final_shock.values())

    print("🔻 Number of stocks that fell:", len(fallen))
    print("🔺 Stocks that rose:", risen)
    print(f"📉 Total network shock: {total_shock:.4f}")

if __name__ == "__main__":
    csv_file = "outputs/correlation_matrix_filtered.csv"  # Replace with your CSV path
    seed_stock = "ADANIENT"  # Replace with your seed stock
    threshold = 0.7  # Ignore weak correlations (adjust as needed)

    G = build_graph_from_correlation_csv(csv_file, threshold=threshold)

    shocks = simulate_shock_propagation(G, seed_stock, initial_shock=-0.05, steps=4, decay=0.2)
    print_shock_results(shocks)
    summarize_shock_effects(shocks)