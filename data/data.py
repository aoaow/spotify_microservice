import pandas as pd

# Load the CSV file
csv_file = "./data/charts.csv"
df = pd.read_csv(csv_file)

# Rename columns for clarity
df.rename(
    columns={
        "title": "track_title",
        "streams": "track_streams",
        "rank": "global_rank",
        "url": "track_url",
    },
    inplace=True,
)

# Convert date to a consistent datetime format
df["date"] = df["date"].dt.strftime("%Y-%m-%d")

# Save the transformed dataset to a Parquet file
output_file = "data/spotify_top_200.parquet"
df.to_parquet(output_file, index=False)

print(f"Data preparation completed and saved as {output_file}")
