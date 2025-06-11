from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from wtforms import FloatField, SubmitField

class PointForm(FlaskForm):
    x = FloatField('X Coordinate', validators=[DataRequired()])
    y = FloatField('Y Coordinate', validators=[DataRequired()])
    submit = SubmitField('Classify')

class AddDataForm(FlaskForm):
    x = FloatField('X Coordinate', validators=[DataRequired()])
    y = FloatField('Y Coordinate', validators=[DataRequired()])
    label = IntegerField('Label (0 or 1)', validators=[DataRequired(), NumberRange(min=0, max=1)])
    submit = SubmitField('Add Data Point')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SurveyForm(FlaskForm):
    feedback = StringField('Your Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')



