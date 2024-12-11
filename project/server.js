import express from 'express';
import cors from 'cors';
import Database from 'better-sqlite3';
import winston from 'winston';

// Setup logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

const app = express();
const db = new Database('spotify.db');

app.use(cors());
app.use(express.json());

// Initialize database
db.exec(`
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
`);

// API Endpoints
app.get('/api/filters', (req, res) => {
  logger.info('Fetching filter options');
  try {
    const regions = db.prepare('SELECT DISTINCT region FROM spotify_tracks').all();
    const artists = db.prepare('SELECT DISTINCT artist FROM spotify_tracks').all();
    const dates = db.prepare('SELECT DISTINCT date FROM spotify_tracks').all();
    
    res.json({
      regions: regions.map(r => r.region),
      artists: artists.map(a => a.artist),
      dates: dates.map(d => d.date)
    });
  } catch (error) {
    logger.error('Error fetching filters:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.get('/api/tracks', (req, res) => {
  const { date, region, artist } = req.query;
  logger.info('Fetching tracks with filters:', { date, region, artist });

  try {
    let query = 'SELECT * FROM spotify_tracks WHERE 1=1';
    const params = [];

    if (date) {
      query += ' AND date = ?';
      params.push(date);
    }
    if (region) {
      query += ' AND region = ?';
      params.push(region);
    }
    if (artist) {
      query += ' AND artist = ?';
      params.push(artist);
    }

    query += ' ORDER BY track_streams DESC LIMIT 200';

    const tracks = db.prepare(query).all(...params);
    res.json(tracks);
  } catch (error) {
    logger.error('Error fetching tracks:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  logger.info(`Server running on port ${PORT}`);
});