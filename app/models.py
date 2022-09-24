# Flask app imports
from app import app, db, login
from flask_login import UserMixin

# Helper libraries
from time import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt

# Flask user authentication
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Flask user models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True, unique=True)                # Username
    email = db.Column(db.String, index=True, unique=True)                   # Email address
    password_hash = db.Column(db.String(128))                               # Password hash
    topics = db.relationship('Topic', backref='author', lazy='dynamic')     # Created forums
    posts = db.relationship('Post', backref='author', lazy='dynamic')       # Created posts
    about_me = db.Column(db.String(140))                                    # User description
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)             # Last seen timestamp in UTC

    # Password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Password hashing decryption
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # User avatars
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # Reset password token
    def get_reset_password_token(self, expires_in=600):     # token expires in 600 seconds
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod   # Called without a class object
    def verify_reset_password_token(token):     # Token decryption
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
# Forum Thread models
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True, unique=True)                       # Forum title
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # Forum timestamp in UTC
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                   # Forum owner reference
    posts = db.relationship('Post', backref='area', lazy='dynamic')             # Forum posts back reference

# Forum Post models
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, index=True)                                     # Post content
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)     # Post timestamp
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))                   # Post owner reference
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))                 # Post in Forum reference

# NDT7 download TCP_INFO data - https://github.com/m-lab/ndt-server/blob/main/spec/ndt7-protocol.md
class Download(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String, index=True)
    month = db.Column(db.String, index=True)
    day = db.Column(db.String, index=True)
    filename = db.Column(db.String, index=True)
    time = db.Column(db.String, index=True)
    client_ip = db.Column(db.String, index=True)
    server_ip = db.Column(db.String, index=True)
    busy_time = db.Column(db.Integer, index=True)
    bytes_acked = db.Column(db.Integer, index=True)
    bytes_received = db.Column(db.Integer, index=True)
    bytes_sent = db.Column(db.Integer, index=True)
    bytes_retrans = db.Column(db.Integer, index=True)
    elapsed_time = db.Column(db.Integer, index=True)
    min_rtt = db.Column(db.Integer, index=True)
    rtt = db.Column(db.Integer, index=True)
    rtt_var = db.Column(db.Integer, index=True)
    rwnd_limited = db.Column(db.Integer, index=True)
    snd_buf_limited = db.Column(db.Integer, index=True)

# NDT7 upload TCP_INFO data - https://github.com/m-lab/ndt-server/blob/main/spec/ndt7-protocol.md
class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String, index=True)
    month = db.Column(db.String, index=True)
    day = db.Column(db.String, index=True)
    filename = db.Column(db.String, index=True)
    time = db.Column(db.String, index=True)
    client_ip = db.Column(db.String, index=True)
    server_ip = db.Column(db.String, index=True)
    busy_time = db.Column(db.Integer, index=True)
    bytes_acked = db.Column(db.Integer, index=True)
    bytes_received = db.Column(db.Integer, index=True)
    bytes_sent = db.Column(db.Integer, index=True)
    bytes_retrans = db.Column(db.Integer, index=True)
    elapsed_time = db.Column(db.Integer, index=True)
    min_rtt = db.Column(db.Integer, index=True)
    rtt = db.Column(db.Integer, index=True)
    rtt_var = db.Column(db.Integer, index=True)
    rwnd_limited = db.Column(db.Integer, index=True)
    snd_buf_limited = db.Column(db.Integer, index=True)