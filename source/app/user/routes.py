# User blueprint routes will go here 
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.forms import EditProfileForm
from app import db
from flask import Blueprint

user = Blueprint('user', __name__)

@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('user.profile'))
    return render_template('user/profile.html', form=form) 