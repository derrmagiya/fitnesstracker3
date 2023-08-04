from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import uuid 
from datetime import datetime 

# Adding Flask Security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import Secrets Module
import secrets

# Import for LoginManager & UserMixin
# helps us login our users & store their credentials
from flask_login import UserMixin, LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String, nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    fitness = db.relationship('Fitness', backref = 'owner', lazy = True)

    def __init__(self, email, username, password, first_name = '', last_name = ''):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token()
        self.username = username 


    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    

    def __repr__(self):
        return f"User {self.email} has been added to the database! Woohoo!"
    

class Fitness(db.Model):
    id = db.Column(db.String, primary_key=True)
    exercise = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(200),nullable = True)
    duration = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Float, nullable=False)
    distance = db.Column(db.Float, nullable=True)
    heart_rate = db.Column(db.Integer, nullable=True)
    steps = db.Column(db.Integer, nullable=True)
    workout_date = db.Column(db.Date, nullable=False)
    workout_time = db.Column(db.Time, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    random_joke = db.Column(db.String, nullable=True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, exercise, description, duration, calories_burned, distance, heart_rate, steps, workout_date, workout_time,
                 notes, random_joke, user_token ):
        self.id = self.set_id()
        self.exercise = exercise
        self.description =description
        self.duration = duration
        self.calories_burned = calories_burned
        self.distance = distance
        self.heart_rate = heart_rate
        self.steps = steps
        self.workout_date = workout_date
        self.workout_time = workout_time
        self.notes = notes
        self.random_joke = random_joke
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"Fitness {self.exercise} has been added to the database! Woohoo!"
    

class FitnessSchema(ma.Schema):
    class Meta:
        fields = ['id', 'exercise', 'description', 'duration', 'calories_burned', 'distance', 'heart_rate',
                  'steps', 'workout_date', 'workout_time', 'notes', 'random_joke']
        
fitness_schema = FitnessSchema()
fitnesses_schema = FitnessSchema(many=True)