from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class UserLoginForm(FlaskForm):
    username = StringField('username', validators = [DataRequired()])
    email = StringField('email', validators = [DataRequired(), Email()])
    password = PasswordField('password', validators = [DataRequired()])
    submit_button = SubmitField()


class FitnessForm(FlaskForm):
    exercise = StringField('Exercise', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=200)])
    duration = IntegerField('Duration (minutes)', validators=[DataRequired(), NumberRange(min=1)])
    calories_burned = IntegerField('Calories Burned', validators=[DataRequired(), NumberRange(min=0)])
    distance = IntegerField('Distance (miles)', validators=[DataRequired(), NumberRange(min=0)])
    heart_rate = IntegerField('Heart Rate (bpm)', validators=[DataRequired(), NumberRange(min=1)])
    steps = IntegerField('Steps', validators=[DataRequired(), NumberRange(min=0)])
    workout_date = StringField('Workout Date', validators=[DataRequired(), Length(max=10)])
    workout_time = StringField('Workout Time', validators=[DataRequired(), Length(max=8)])
    notes = StringField('Notes', validators=[Length(max=500)])
    random_joke =StringField('random joke')
    submit_button = SubmitField()
    
