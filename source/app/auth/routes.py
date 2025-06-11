from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import User
from .forms import SurveyForm, AddDataForm



bp = Blueprint('auth', __name__, template_folder='../../templates')

@bp.route('/add-data', methods=['GET', 'POST'])
def add_data():
    form = AddDataForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        label = form.label.data
        flash('Data point added!', 'success')
        return redirect(url_for('main.home'))
    return render_template('main/add_data.html', form=form)


@bp.route('/survey', methods=['GET', 'POST'])
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        feedback = form.feedback.data
        flash('Thank you for your feedback!', 'success')
        return redirect(url_for('main.home'))
    return render_template('main/survey.html', form=form)



@bp.route('/Login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash(message='Invalid credentials. Please try again.', category='danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.home'))


    return render_template('auth/login.html')






@bp.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', category='danger')
            return redirect(url_for('auth.signup'))


        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', category='success')
        return redirect(url_for('auth.login'))

    return render_template('auth/signup.html')




@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))