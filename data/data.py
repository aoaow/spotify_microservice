import pandas as pd

# Load the CSV file
csv_file = "./data/charts.csv"
df = pd.read_csv(csv_file)

# Filter to keep only the top 15 regions by total streams
top_regions = df.groupby("region")["streams"].sum().nlargest(15).index.tolist()
df = df[df["region"].isin(top_regions)]

# Filter to keep data only from specific years
years_to_keep = [2020, 2021]
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"].dt.year.isin(years_to_keep)]

# Calculate average streams per artist
df["avg_streams"] = df.groupby("artist")["streams"].transform("mean")

# Add rankings by streams within each region and date
df["rank_by_region"] = df.groupby(["region", "date"])["streams"].rank(
    method="min", ascending=False
)

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
