from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PointInputForm(FlaskForm):
    points = TextAreaField(
        'Enter points (x, y, label):',
        validators=[DataRequired()],
        render_kw={"placeholder": "Example:\n1.0,2.0,1\n2.0,3.0,-1"}
    )
    submit = SubmitField('Classify')
