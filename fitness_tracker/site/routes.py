from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from fitness_tracker.forms import FitnessForm 
from fitness_tracker.models import Fitness, db
from fitness_tracker.helpers import random_joke_generator


site = Blueprint('site', __name__, template_folder='site_templates')


@site.route('/')
def home():
    print('look at this cool project. Would you just look at it')
    return render_template('index.html')

@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    fitnessform = FitnessForm()

    try:
        if request.method == 'POST' and fitnessform.validate_on_submit():
            exercise = fitnessform.exercise.data
            description = fitnessform.description.data
            duration = fitnessform.duration.data
            calories_burned = fitnessform.calories_burned.data
            distance = fitnessform.distance.data
            heart_rate = fitnessform.heart_rate.data
            steps = fitnessform.steps.data
            workout_date = fitnessform.workout_date.data
            workout_time = fitnessform.workout_time.data
            notes = fitnessform.notes.data
            if fitnessform.random_joke.data:
                random_joke = fitnessform.random_joke.data
            else:
                random_joke = random_joke_generator()
            user_token = current_user.token

            fitness = Fitness(exercise, description, duration, calories_burned, distance, heart_rate, steps, 
                              workout_date, workout_time, notes, random_joke, user_token)
            
            print(fitness)
            db.session.add(fitness)
            db.session.commit()

            return redirect(url_for('site.profile'))
        
    except:
        raise Exception('Fitness not created, please check your form and try again.')
    
    user_token = current_user.token
    fitnesses = Fitness.query.filter_by(user_token=user_token)

    return render_template('/profile.html', form=fitnessform, fitnesses=fitnesses )