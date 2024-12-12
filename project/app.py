import sys
import os
# Add the parent directory of 'project' to the module search path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from config.database import init_db, load_data_from_df, process_spotify_data
from models.track import Track
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/health')
def health():
    return "OK", 200

# Initialize the database schema
init_db()

# Preprocess and load data from parquet
df = pd.read_parquet('data/spotify_top_200.parquet')
df = process_spotify_data(df)
load_data_from_df(df)


@app.route('/filters', methods=['GET'])
def get_filters():
    print("Request received for /filters")
    try:
        filters = Track.get_filters()  # Log here if necessary
        print("Filters processed successfully")
        return jsonify(filters)
    except Exception as e:
        print(f"Error in /filters: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/tracks', methods=['GET'])
def get_tracks():
    print("Request received for /tracks")
    try:
        date = request.args.get('date')
        region = request.args.get('region')
        artist = request.args.get('artist')
        tracks = Track.get_tracks(date=date, region=region, artist=artist)
        print("Tracks processed successfully")
        return jsonify(tracks)
    except Exception as e:
        print(f"Error in /tracks: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """
    Renders the index.html file as the main page.
    """
    return render_template('index.html')

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Unhandled exception: {e}")
    return jsonify({"error": "Internal Server Error"}),