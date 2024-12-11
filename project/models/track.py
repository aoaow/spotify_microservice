from config.database import get_db_connection
from config.logger import setup_logger

logger = setup_logger()

class Track:
    @staticmethod
    def get_filters():
        """Get all available filter options."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get distinct values for filters
            regions = cursor.execute('SELECT DISTINCT region FROM spotify_tracks').fetchall()
            artists = cursor.execute('SELECT DISTINCT artist FROM spotify_tracks').fetchall()
            dates = cursor.execute('SELECT DISTINCT date FROM spotify_tracks').fetchall()

            return {
                'regions': [row['region'] for row in regions],
                'artists': [row['artist'] for row in artists],
                'dates': [row['date'] for row in dates]
            }
        except Exception as e:
            logger.error(f"Error fetching filters: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    def get_tracks(date=None, region=None, artist=None):
        """Get tracks based on filters."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = 'SELECT * FROM spotify_tracks WHERE 1=1'
            params = []

            if date:
                query += ' AND date = ?'
                params.append(date)
            if region:
                query += ' AND region = ?'
                params.append(region)
            if artist:
                query += ' AND artist = ?'
                params.append(artist)

            query += ' ORDER BY track_streams DESC LIMIT 200'

            tracks = cursor.execute(query, params).fetchall()
            return [dict(track) for track in tracks]
        except Exception as e:
            logger.error(f"Error fetching tracks: {e}")
            raise
        finally:
            conn.close()

    @staticmethod
    def has_data():
        """Check if spotify_tracks table has any data."""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) as count FROM spotify_tracks')
            result = cursor.fetchone()
            return result['count']
        except Exception as e:
            logger.error(f"Error checking data availability: {e}")
            raise
        finally:
            conn.close()