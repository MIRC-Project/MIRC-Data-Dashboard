# Flask and Database Imports
from app import app, db
from flask import render_template

@app.errorhandler(404)          # Error 404 webpage
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)          # Error 500 webpage
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500