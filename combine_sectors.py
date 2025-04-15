import os
import pandas as pd

# Define the folder containing your CSVs
folder_path = "sectors"

# Set to store unique (Symbol, Industry) pairs
unique_entries = set()

# Loop through each CSV file
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        try:
            df = pd.read_csv(file_path, usecols=["Symbol", "Industry"])
            for _, row in df.iterrows():
                symbol = row["Symbol"]
                industry = row["Industry"]
                unique_entries.add((symbol, industry))
        except ValueError as e:
            print(f"Skipping {filename} due to missing expected columns: {e}")

# Convert set to DataFrame
unique_df = pd.DataFrame(list(unique_entries), columns=["Symbol", "Industry"])

# Save to CSV
unique_df.to_csv("outputs/combined_sectors.csv", index=False)

print("Final CSV saved as 'combined_sectors.csv' (only one entry per unique Symbol-Industry pair)")
