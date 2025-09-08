from jose import jwt 
import jose
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
import os


SECRET_KEY = os.environ.get('SECRET_KEY') or 'dont tell anyone'

def encode_token(mechanic_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        'iat': datetime.now(timezone.utc),
        'sub': str(mechanic_id)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    @wraps(f)
    def decoration(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
            #SELF REMINDER:
            #Accesses the headers, then the "Bearer token" string, 
            # we then split into ['Bearer', 'token'], we then index into token

        if not token:
            return jsonify({"error": "Token missing from authorization headers"}), 401
        

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.mechanic_id = int(data['sub'])
        except jose.exceptions.ExpiredSignatureError:
            return jsonify({"message": 'Token is expired'}), 403
        except jose.exceptions.JWTError:
            return jsonify({"message": 'Invalid token'}), 403
        
        return f(*args,**kwargs)
    
    return decoration




#For practice implement token authentication for your Mechanic shop.

# Create an encode_token function that takes in a mechanic_id to create a 
# token specific to that user.
# add a password field to you Mechanics model. (Drop all tables using db.drop_all())
# login_schema, which can be made by excluding all fields except email and 
# password from your MechanicSchema
# In your mechanics blueprint, create a login route:
# POST '/login' : passing in email and password, validated by login_schema
# After credentials have been validate utilizes the encode_token() function 
# to make a token to be returned to that customer.


# Create @token_required wrapper, that validates and unpacks the token, 
# and stores the id in the request as a field. 

# Create a route that requires a token, that returns the 
# service_tickets related to that mechanic.


# GET '/my-tickets': requires a Bearer Token authorization. (OPTIONAL... for now will be required in the end project)
# The route function should extract the mechanic_id from the request.
# Using that id query the service_tickets that belong to the mechanic.

# Additionally add @token_required to any routes you think should require 
# authorization. (ex: Update, Delete,...)

