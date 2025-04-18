import pandas as pd
import numpy as np

def adjacency_filtered(file_name):

    # Load cleaned stock data
    df = pd.read_csv("outputs/" + file_name + ".csv")

    # Load list of relevant stock symbols
    sector_df = pd.read_csv("outputs/combined_sectors.csv")
    selected_symbols = sector_df['Symbol'].unique()

    # Filter stock data to include only selected symbols
    df_filtered = df[["Date"] + [sym for sym in selected_symbols if sym in df.columns]]

    # Drop the 'Date' column for correlation calculations
    stock_data = df_filtered.drop(columns=['Date'])

    # Compute Pearson correlation matrix
    correlation_matrix = stock_data.corr()

    # Set diagonal to 0 (correlation of a stock with itself)
    np.fill_diagonal(correlation_matrix.values, 0)

    # Save correlation matrix (optional)
    correlation_matrix.to_csv("outputs/correlation_matrix_filtered.csv")

    # Define threshold and build adjacency matrix
    threshold = 0.9
    adjacency_matrix = (correlation_matrix.abs() > threshold).astype(int)

    # Save adjacency matrix
    adjacency_matrix.to_csv("outputs/adjacency_matrix_filtered.csv")

    print("Adjacency matrix created for selected stock symbols.")
