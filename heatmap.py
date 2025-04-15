import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_correlation_heatmap(csv_path):
    # Load the correlation matrix
    corr_matrix = pd.read_csv(csv_path, index_col=0)

    # Set up the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=False, fmt=".2f", cmap="coolwarm", square=True, linewidths=0.5)
    plt.title("Correlation Matrix Heatmap")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_correlation_heatmap("outputs/correlation_matrix_filtered.csv")
