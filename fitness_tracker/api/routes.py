from flask import Blueprint, request, jsonify
from fitness_tracker.helpers import token_required, random_joke_generator
from fitness_tracker.models import db, Fitness, fitness_schema, fitnesses_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'some': 'value'}

# Create Fitness Endpoint
@api.route('/fitnesses', methods=['POST'])
@token_required
def create_fitness(our_user):

    exercise = request.json['exercise']
    description = request.json['description']
    duration = request.json['duration']
    calories_burned = request.json['calories_burned']
    distance = request.json['distance']
    heart_rate = request.json['heart_rate']
    steps = request.json['steps']
    workout_date = request.json['workout_date']
    workout_time = request.json['workout_time']
    notes = request.json['notes']
    random_joke = random_joke_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    fitness = Fitness(exercise, description, duration, calories_burned, distance, heart_rate, steps, workout_date,
                      workout_time, notes, random_joke, user_token)

    db.session.add(fitness)
    db.session.commit()

    response = fitness_schema.dump(fitness)

    return jsonify(response)

#Read 1 Single Fitness Endpoint
@api.route('/fitnesses/<id>', methods = ['GET'])
@token_required
def get_fitness(our_user, id):
    if id:
        fitness = Fitness.query.get(id)
        response = fitness_schema.dump(fitness)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    

#Read all the Fitnesses
@api.route('/fitnesses', methods = ['GET'])
@token_required
def get_fitnesses(our_user):
    token = our_user.token
    fitnesses = Fitness.query.filter_by(user_token = token).all()
    response = fitnesses_schema.dump(fitnesses)

    return jsonify(response)


#Updeate 1 Drone by ID
@api.route('/drones/<id>', methods = ['PUT'])
@token_required
def update_drone(our_user,id):
    fitness = Fitness.query.get(id)

    fitness.exercise = request.json['exercise']
    fitness.description = request.json['description']
    fitness.duration = request.json['duration']
    fitness.calories_burned = request.json['calories_burned']
    fitness.distance = request.json['distance']
    fitness.heart_rate = request.json['heart_rate']
    fitness.steps = request.json['steps']
    fitness.workout_date = request.json['workout_date']
    fitness.workout_time = request.json['workout_time']
    fitness.notes = request.json['notes']
    fitness.random_joke = random_joke_generator()
    fitness.user_token = our_user.token

    db.session.commit()

    response = fitness_schema.dump(fitness)

    return jsonify(response)


#Delete 1 Fitness by ID
@api.route('/fitnesses/<id>', methods = ['DELETE'])
@token_required
def delete_fitness(our_user, id):
    fitness = Fitness.query.get(id)
    db.session.delete(fitness)
    db.session.commit()

    response = fitness_schema.dump(fitness)

    return jsonify(response)


