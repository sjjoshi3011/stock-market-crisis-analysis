import os
import pandas as pd

# Set path to your directory of CSVs
folder_path = "NSE_dataset"
outpath = "outputs/all_stocks_closing_prices_2019.csv"
# Create a date range for index
date_range = pd.date_range(start="2019-01-01", end="2020-01-01", freq='D')
final_df = pd.DataFrame({'Date': date_range})
final_df['Date'] = final_df['Date'].dt.date  # remove time from datetime

# Set 'Date' as index for merging
final_df.set_index('Date', inplace=True)

# Process each CSV file
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        stock_name = filename.replace(".NS.csv", "")
        file_path = os.path.join(folder_path, filename)

        df = pd.read_csv(file_path, usecols=[0, 4], names=['Date', 'Close'], header=0)
        df['Date'] = pd.to_datetime(df['Date'].str.split(' ').str[0])  # Keep only the date part
        df = df[(df['Date'] >= '2019-01-01') & (df['Date'] <= '2020-01-01')]
        df.set_index('Date', inplace=True)
        df.rename(columns={'Close': stock_name}, inplace=True)

        final_df = final_df.join(df, how='left')

# Reset index and export to CSV
final_df.reset_index(inplace=True)
final_df.to_csv(outpath, index=False)
