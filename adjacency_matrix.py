import pandas as pd
import numpy as np

if __name__ == '__main__':
    # Load cleaned stock data
    df = pd.read_csv("outputs/all_stocks_closing_prices_2020_cleaned.csv")

    # Drop the 'Date' column for correlation calculations
    stock_data = df.drop(columns=['Date'])

    # Compute Pearson correlation matrix
    correlation_matrix = stock_data.corr()

    # Set diagonal to 0 (correlation of a stock with itself)
    np.fill_diagonal(correlation_matrix.values, 0)

    # Save correlation matrix (optional)
    correlation_matrix.to_csv("outputs/correlation_matrix.csv")

    # Define threshold and build adjacency matrix
    threshold = 0.9
    adjacency_matrix = (correlation_matrix.abs() > threshold).astype(int)

    # Save adjacency matrix
    adjacency_matrix.to_csv("outputs/adjacency_matrix.csv")
