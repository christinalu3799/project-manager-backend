import models

from flask import request, jsonify, Blueprint, session
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from playhouse.shortcuts import model_to_dict
from flask_cors import cross_origin

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
        session['user'] = user_dict
        print('---THIS IS THE USER SESSION (REGISTER): ', session['user'])

        del user_dict['password']

        if 'user' in session:
            user = session['user']
            return jsonify(data = user, status = {
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
            print('The current user_dict is: ', user_dict)
            print('is current user authenticated?', current_user.is_authenticated)
            return jsonify(data=user_dict, status={
                "code": 200, 
                "message": "Successfully logged in."
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
# ================================================================
@user.route('/get_all_users', methods = ['GET'])
def get_all_users(): 
    all_users = models.User.select()
    all_users_dict = [model_to_dict(user) for user in all_users]
    return jsonify(data=all_users_dict), 200