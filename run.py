# run.py
import os
from app import create_app
from config import config

# Get environment from environment variable, default to 'development'
env = os.environ.get('FLASK_ENV', 'development')
app = create_app()

if __name__ == '__main__':
    # Load configuration based on environment
    app.config.from_object(config[env])
    
    # Run the app - bind to localhost specifically
    app.run(
        host='127.0.0.1',  # Changed from 0.0.0.0 to 127.0.0.1
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )