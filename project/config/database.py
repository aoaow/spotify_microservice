import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
import sqlite3
import pandas as pd
from project.config.logger import setup_logger


logger = setup_logger()


def get_db_connection():
    """Create a database connection."""
    try:
        conn = sqlite3.connect('spotify.db', check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_db():
    """Initialize the database with required tables."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create tracks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spotify_tracks (
                track_title TEXT,
                global_rank INTEGER,
                date TEXT,
                artist TEXT,
                track_url TEXT,
                region TEXT,
                chart TEXT,
                trend TEXT,
                track_streams REAL,
                avg_streams REAL,
                rank_by_region REAL
            )
        ''')

        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        conn.close()

def load_data_from_df(df):
    try:
        conn = get_db_connection()
        df.to_sql('spotify_tracks', conn, if_exists='replace', index=False)
        logger.info("Successfully loaded DataFrame into database")
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise
    finally:
        conn.close()

def process_spotify_data(df):
    """Process Spotify data before loading into database."""
    try:
        # Remove duplicates
        df = df.drop_duplicates()

        # Sort by streams
        df = df.sort_values('track_streams', ascending=False)

        # Calculate average streams per region
        df['avg_streams'] = df.groupby('region')['track_streams'].transform('mean')

        # Calculate rank by region
        df['rank_by_region'] = df.groupby('region')['track_streams'].rank(ascending=False)

        df = df.drop_duplicates(subset=['track_title', 'artist', 'region', 'date'])

        return df
        

    except Exception as e:
        logger.error(f"Error processing data: {e}")
        raise