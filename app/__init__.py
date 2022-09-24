# Flask imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_moment import Moment

# Logging
import logging
from logging.handlers import RotatingFileHandler
import os

# Configuration
from config import Config

app = Flask(__name__)                       # Flask app instantiation
app.config.from_object(Config)              # Configuration variables
db = SQLAlchemy(app)                        # Flask SQLAlchemy
migrate = Migrate(app, db)                  # Flask SQLAlchemy database migrations
login = LoginManager(app)                   # Flask login authenticator
moment = Moment(app)                        # Flask Local Timezone conversion
scheduler = APScheduler()                   # Flask APScheduler instantiation
scheduler.init_app(app)                     # Flask APScheduler added to Flask app
scheduler.start()                           # Flask APScheduler started

# Logging via Rotating File Handler
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/mirc-data-dashboard.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('MIRC Data Dashboard startup')

from app import routes, models, errors