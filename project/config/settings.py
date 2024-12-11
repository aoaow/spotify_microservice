import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Flask settings
FLASK_APP = os.getenv('FLASK_APP', 'app.py')
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///spotify.db')

# Application settings
DEBUG = FLASK_ENV == 'development'
PORT = int(os.getenv('PORT', 3000))
HOST = os.getenv('HOST', '0.0.0.0')