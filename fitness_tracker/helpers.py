from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

from fitness_tracker.models import User  


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        """
        This function takes in any number of args and kwargs and verifies that the token passed into 
        the headers is associated with a user in the database.
        """
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401 #Client error

        try:
            our_user = User.query.filter_by(token=token).first()  
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is Invalid'}), 401 #Client error
            
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated


class JSONEncoder(json.JSONDecodeError):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONDecodeError(JSONEncoder, self).default(obj)
    

def random_joke_generator():
    
    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
	    "X-RapidAPI-Key": "5024377859msh30b2cca49348195p1468a4jsnc4f135ba5800",
	    "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    return data['body'][0]['setup'] + ' ' + data['body'][0]['punchline']