from flask import Blueprint, jsonify, request
from models.track import Track
from config.logger import setup_logger

logger = setup_logger()
track_bp = Blueprint('tracks', __name__)

@track_bp.route('/filters', methods=['GET'])
def get_filters():
    """Endpoint to get all filter options."""
    try:
        filters = Track.get_filters()
        return jsonify(filters)
    except Exception as e:
        logger.error(f"Error in get_filters endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@track_bp.route('/tracks', methods=['GET'])
def get_tracks():
    """Endpoint to get filtered tracks."""
    try:
        date = request.args.get('date')
        region = request.args.get('region')
        artist = request.args.get('artist')

        logger.info(f"Fetching tracks with filters: date={date}, region={region}, artist={artist}")
        
        tracks = Track.get_tracks(date, region, artist)
        return jsonify(tracks)
    except Exception as e:
        logger.error(f"Error in get_tracks endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500