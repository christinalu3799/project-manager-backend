import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from playhouse.shortcuts import model_to_dict

# ================================================================
user = Blueprint('users', 'user')
# ================================================================
@user.route('/register', methods=['POST'])
def register():
    payload = request.get_json() 
    payload['email'] = payload['email'].lower()
    try: 
        models.User.get(models.User.email == payload['email'])
        return jsonify(data={},status={
            "code": 401, 
            "message": "A user with that name already exists"
        })
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload) # add new user to database

        # start user session
        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)

        del user_dict['password']
        return jsonify(data = user_dict, status = {
            "code": 201,
            "message": "Successfully registered new user."
        })
# ================================================================
@user.route('/login', methods=['POST'])
def login(): 
    payload = request.get_json()
    print('payload', payload)
    try:
        user = models.User.get(models.User.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print('The current user is: ', user)
            return jsonify(data={}, status={
                "code": 200, 
                "message": "Successfully logged in."
            })
        else:
            return jsonify(data=user, status={
                "code": 401,
                "message": "Sorry, Username or Password is incorrect."
            })
    except models.DoesNotExist:
        return jsonify(data={}, status={
            "code": 401,
            "message": "Sorry, Username or Password is incorrect."
        })
# ================================================================
@user.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify(
        data={},
        status=200,
        message='User successfully logged out.'
    ), 200
# ================================================================
@user.route('/logged_in_user', methods = ['GET'])
def get_logged_in_user(): 
    print(f"{current_user.username} is current_user.username in GET logged_in_user")
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')
    return jsonify(data=user_dict), 200