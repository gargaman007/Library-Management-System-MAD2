from flask import current_app as app, jsonify, request, make_response
from db.models import User
from security_framework import current_user
from flask_restful import Resource
from flask_security import auth_token_required

class UserProfileResource(Resource):
    @auth_token_required
    def get(self):
        user_id = current_user.id
        # Retrieve user information from the database
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        # Return user profile information
        profile_info = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'last_login_at': user.last_login_at,
            'current_login_at': user.current_login_at,
            'last_login_ip': user.last_login_ip,
            'current_login_ip': user.current_login_ip,
            'login_count': user.login_count,
            'active': user.active,
            'confirmed_at': user.confirmed_at
        }
        return make_response(jsonify(profile_info), 200)