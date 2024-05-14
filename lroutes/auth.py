from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import user_datastore, bcrypt, login_user, roles_accepted, login_function, current_user
from flask_restful import Resource


class register(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        try:
            user_user = user_datastore.create_user(email=email, password=hashed_password)
            user_datastore.add_role_to_user(user_user, 'user')
            db.session.commit()
            user_id = User.query.filter_by(email=email).first().id
            activity = UserActivity(user_id=user_id, activity_type='registered')
            db.session.add(activity)
            db.session.commit()
            return make_response(jsonify({'message': 'User has been registered successfully'}), 200)
        except:
            # Handle the case when the email already exists
            return make_response(jsonify({'message': 'This email is already registered. Please use a different email.'}), 400)       

class login(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = user_datastore.find_user(email=email)

        if login_function(email, password):
            auth_token = user.get_auth_token()
            return make_response(jsonify({'message': 'User logged in successfully', 'auth_token': auth_token, 'id': current_user.id,
                'email': current_user.email,
                'roles': [role.name for role in current_user.roles]}), 200)
        else:
            return make_response(jsonify({'message': 'Invalid email or password.'}), 400)

class logout(Resource):
    @roles_accepted('admin', 'user')
    def get(self):
        activity = UserActivity(user_id=current_user.id, activity_type='logout')
        db.session.add(activity)
        db.session.commit()
        return make_response(jsonify({'message': 'User logged out successfully'}), 200)