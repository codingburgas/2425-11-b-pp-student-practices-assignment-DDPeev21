# Error handlers will go here 
from flask import render_template
from app.errors import errors

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500 