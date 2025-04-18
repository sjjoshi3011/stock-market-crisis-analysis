import pandas as pd

def preprocess(file_name):
    # Load the merged CSV file
    file_path = "outputs/" + file_name + ".csv"
    df = pd.read_csv(file_path)

    # Drop columns where the second row (index 1) has missing values
    df1 = df.dropna(axis=1, subset=[1])

    # Identify the second column (after 'Date')
    second_column = df1.columns[1]

    # Drop rows where the second column has missing values
    df2 = df1.dropna(subset=[second_column])

    # Drop columns (excluding 'Date') that have any missing values
    df3 = df2.dropna(axis=1, how='any')

    # Save the cleaned DataFrame to a new CSV file
    output_path = "outputs/" + file_name + "_cleaned.csv"
    df3.to_csv(output_path, index=False)


