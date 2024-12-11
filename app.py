from flask import Flask, jsonify, request
import pandas as pd
import logging

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler(),  # Log to console
    ],
)

# Load the Parquet dataset
df = pd.read_parquet("data/spotify_top_200.parquet")

# Precompute grouped data for faster lookups
grouped_data = {
    (region, date): group for (region, date), group in df.groupby(["region", "date"])
}

artist_data = {artist: group for artist, group in df.groupby("artist")}


@app.before_request
def log_request_info():
    """Log information about each incoming request."""
    logging.info("Request: %s %s", request.method, request.url)
    if request.args:
        logging.info("Query Parameters: %s", request.args)


@app.route("/", methods=["GET"])
def home():
    logging.info("Home endpoint accessed")
    return "Welcome to the Spotify Top 200 Microservice!"


@app.route("/rankings", methods=["GET"])
def get_rankings():
    region = request.args.get("region", type=str)
    date = request.args.get("date", type=str)
    limit = request.args.get("limit", default=10, type=int)

    key = (region, date)
    if key not in grouped_data:
        logging.warning("No data found for region: %s, date: %s", region, date)
        return jsonify([])

    filtered_data = grouped_data[key].nsmallest(limit, "rank_by_region")
    result = filtered_data[
        ["track_title", "artist", "region", "track_streams", "rank_by_region"]
    ].to_dict(orient="records")
    logging.info("Returned %d results for region: %s, date: %s", len(result), region, date)
    return jsonify(result)


@app.route("/artist", methods=["GET"])
def get_artist_data():
    artist = request.args.get("artist", type=str)
    limit = request.args.get("limit", default=10, type=int)
    offset = request.args.get("offset", default=0, type=int)

    if not artist or artist not in artist_data:
        logging.error("Artist not found: %s", artist)
        return jsonify({"error": "Artist not found"}), 404

    artist_group = artist_data[artist].iloc[offset : offset + limit]
    result = artist_group[
        ["track_title", "date", "region", "track_streams", "rank_by_region"]
    ].to_dict(orient="records")
    logging.info("Returned %d records for artist: %s", len(result), artist)
    return jsonify(result)


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle unexpected errors and log them."""
    logging.error("An error occurred: %s", str(e))
    return jsonify({"error": "Internal Server Error"}), 500


# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
