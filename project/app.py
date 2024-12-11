from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from config.database import init_db, load_data_from_df, process_spotify_data
from models.track import Track
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initialize the database schema
init_db()

# Preprocess and load data from parquet
df = pd.read_parquet('data/spotify_top_200.parquet')
df = process_spotify_data(df)
load_data_from_df(df)


@app.route('/filters', methods=['GET'])
def get_filters():
    """
    API endpoint to get filter options: dates, regions, and artists.
    """
    try:
        filters = Track.get_filters()
        return jsonify(filters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tracks', methods=['GET'])
def get_tracks():
    """
    API endpoint to get tracks filtered by date, region, and artist.
    """
    date = request.args.get('date')
    region = request.args.get('region')
    artist = request.args.get('artist')

    try:
        tracks = Track.get_tracks(date=date, region=region, artist=artist)
        response = [
            {
                'rank': index + 1,
                'track_title': track['track_title'],
                'artist': track['artist'],
                'streams': track['track_streams'],
                'track_url': track['track_url'],
            }
            for index, track in enumerate(tracks)
        ]
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def index():
    """
    Renders the index.html file as the main page.
    """
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)