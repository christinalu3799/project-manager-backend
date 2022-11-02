import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
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

        # del user_dict['password']
        return jsonify(data = user, status = {
            "code": 201,
            "message": "Successfully registered new user."
        })

