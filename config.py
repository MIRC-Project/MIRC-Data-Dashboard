import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Secure Form token
    SECRET_KEY = 'you-will-never-guess'

    # SQLite database location
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    # SQLAlchemy track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Paginated items per page - forum titles and forum posts 
    ITEMS_PER_PAGE = 10

    # FlaskAPScheduler Status
    SCHEDULER_API_ENABLED = True
    
    # Sendgrid API key
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER = ''

    # Dropbox API
    APP_KEY = "",
    APP_SECRET = "",
    OAUTH2_REFRESH_TOKEN = ""