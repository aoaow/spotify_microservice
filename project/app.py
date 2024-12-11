from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from config.database import init_db, load_data_from_df, process_spotify_data
import pandas as pd

# Initialize the database schema
init_db()

# Preprocess and load data from parquet
df = pd.read_parquet('data/spotify_top_200.parquet')
df = process_spotify_data(df)
# df now has the processed data, load it into the database
load_data_from_df(df)

from flask import Flask, jsonify, request
from models.track import Track  # assuming you've placed Track there

@app.route('/filters', methods=['GET'])
def get_filters():
    try:
        filters = Track.get_filters()
        return jsonify(filters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tracks', methods=['GET'])
def get_data():
    date = request.args.get('date')
    region = request.args.get('region')
    artist = request.args.get('artist')

    try:
        tracks = Track.get_tracks(date=date, region=region, artist=artist)
        return jsonify(tracks)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)