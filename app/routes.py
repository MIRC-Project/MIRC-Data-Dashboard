# Flask app imports
from app import app, db, scheduler
from app.database import dropbox_storage
from app.graph import throughput, min_round_trip, avg_round_trip
from app.forms import Date, RegistrationForm, LoginForm, Forum, Comments, EditProfileForm
from app.models import Download, User, Topic, Post
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm

# Flask Template Engine
from flask import render_template, url_for, redirect, flash, request

# Flask Login Authentication
from flask_login import current_user, login_user, logout_user

# Helper Libraries
from datetime import datetime

# Flask APScheduler - Calls 'dropbox_storage()' from database.py every 5 minutes
@scheduler.task('interval', id='do_job_1', seconds=360)
def update():
    print('begin')
    dropbox_storage()
    print('done')

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])       # Index page
def index():
    form = Date()       # NDT7 test date selector form
    # dates - Record of all NDT7 measurement timestamps
    dates = Download.query.with_entities(Download.year, Download.month, Download.day).order_by(Download.year, Download.month, Download.day).all()
    
    # Unpacks 'dates' and filters for unique entries
    tmp = []
    j = 0
    for item in dates:
        if j == 0:
            tmp.append(item)
            j += 1
        else:
            if item == tmp[-1]:
                continue
            else:
                tmp.append(item)
    dates = tmp

    # Date selector validation
    if form.validate_on_submit():
        y = form.year.data
        m = form.month.data
        d = form.day.data
        return redirect(url_for('graph',year=y, month=m, day=d))
    return render_template('index.html', title='Data Dashboard', form=form, dates=dates)

@app.route('/forum', methods=['GET', 'POST'])       # Forum Root page
def forum():
    form = Forum()          # Forum creation form
    
    # Forum creation validation
    if form.validate_on_submit():
        discussion = Topic(title=form.title.data, author=current_user)
        db.session.add(discussion)
        db.session.commit()
        return redirect(url_for('forum'))

    # Pagination
    page = request.args.get('page', 1, type=int)
    topics = Topic.query.order_by(Topic.timestamp.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('forum', page=topics.next_num) \
        if topics.has_next else None
    prev_url = url_for('forum', page=topics.prev_num) \
        if topics.has_prev else None

    return render_template('forum.html', title='Forum', topics=topics, form=form, next_url=next_url, prev_url=prev_url)

@app.route('/forum/<post>', methods=['GET', 'POST'])        # Forum subpages
def post(post):
    # Forum entity for reference to encapsulated posts
    topic = Topic.query.filter_by(title=post).first()
    
    form = Comments()       # Forum posts form

    # Forum posts validation
    if form.validate_on_submit():
        comment = Post(body=form.body.data, author=current_user, area=topic)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post=post))
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(topic_id=topic.id).order_by(Post.timestamp.asc()).paginate(page, app.config['ITEMS_PER_PAGE'], False)
    next_url = url_for('post', post=post, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('post', post=post, page=posts.prev_num) \
        if posts.has_prev else None

    return render_template('posts.html', title=post, posts=posts, form=form, next_url=next_url, prev_url=prev_url)

@app.route('/about')        # About page
def about():
    return render_template("about.html", title="About")

@app.route('/data/<year>/<month>/<day>', methods=['GET', 'POST'])       # Data Dashboard page
def graph(year, month, day):
    # dates - Record of all NDT7 measurement timestamps
    dates = Download.query.with_entities(Download.year, Download.month, Download.day).order_by(Download.year, Download.month, Download.day).all()
    
    # Unpacks 'dates' and filters for unique entries
    tmp = []
    j = 0
    for item in dates:
        if j == 0:
            tmp.append(item)
            j += 1
        else:
            if item == tmp[-1]:
                continue
            else:
                tmp.append(item)
    dates = tmp
    
    form = Date()   # NDT7 test date selector form
    # Date selector validation
    if form.validate_on_submit():
        y = form.year.data
        m = form.month.data
        d = form.day.data
        return redirect(url_for('graph',year=y, month=m, day=d))
    
    # Function Calls - Data plots 
    throughput(year, month, day)
    min_round_trip(year, month, day)
    avg_round_trip(year, month, day)
    return render_template("graph.html", title="Server-Side Visualization", form=form, dates=dates)

@app.route('/login', methods=['GET', 'POST'])       # Login page
def login():
    # Checks if user is logged-in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()      # User login form
    
    # Login form validation
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')       # logout request
def logout():
    logout_user()           # logs out logged-in user
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])        # Registration page
def register():
    # If user is logged in, redirect to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()       # User registration form

    # Registration form validation   
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')      # User profile page
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.before_request     # Called for every request
def before_request():   # Sets the logged-in user's last seen timestamp
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])        # Edit profile page
def edit_profile():
    form = EditProfileForm(current_user.username)       # Edit profile form
    
    # Edit profile form validation
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=form.username.data))
    # retrieve current user profile info
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])      # Password Reset Request page 
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()       # Password reset request form
    
    # Password request form validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])      # Password reset page
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # Password reset token verification
    user = User.verify_reset_password_token(token)

    # If verification failed or unrecognized
    if not user:
        return redirect(url_for('index'))

    form = ResetPasswordForm()      # Password reset form

    # Password reset form validation
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)