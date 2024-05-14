from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import current_user
from flask_restful import Resource
from flask_security import roles_accepted, auth_token_required, roles_required, auth_required
from datetime import datetime
from datetime import timedelta
from .cache import cache

class FeedbackResource(Resource):
    def get(self):
        user_id = current_user.id
        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)
        
        # Get all feedback given by the user
        feedback = Feedback.query.filter_by(user_id=user_id).all()
        feedback_info = [
            {
                'id': fb.id,
                'issue_id': fb.issue_id,
                'feedback': fb.feedback
            }
            for fb in feedback
        ]
        return make_response(jsonify(feedback_info), 200)
    
    def post(self):
        user_id = current_user.id
        data = request.get_json()
        issue_id = data.get('issue_id')
        feedback_text = data.get('feedback')
        
        # Check if the issue exists and is associated with the user
        issue = Issue.query.filter_by(id=issue_id, user_id=user_id).first()
        if not issue:
            return make_response(jsonify({'message': 'Issue not found or does not belong to the user'}), 404)
        
        # Check if the issue is returned
        if issue.status != 'returned':
            return make_response(jsonify({'message': 'Feedback can only be submitted for returned issues'}), 400)

        # Check if feedback for this issue already exists
        existing_feedback = Feedback.query.filter_by(issue_id=issue_id).first()
        if existing_feedback:
            return make_response(jsonify({'message': 'Feedback already exists for this issue'}), 400)

        # Create new feedback
        new_feedback = Feedback(issue_id=issue_id, user_id=user_id, feedback=feedback_text)
        db.session.add(new_feedback)

        db.session.commit()
        return make_response(jsonify({'message': 'Feedback created successfully'}), 201)
        


class AllFeedbackResource(Resource):
    @cache.cached(timeout=10)
    def get(self):
        # Get all feedback
        all_feedback = Feedback.query.all()
        
        # Format feedback data
        feedback_info = [
            {
                'id': feedback.id,
                'issue_id': feedback.issue_id,
                'user_id': feedback.user_id,
                'feedback': feedback.feedback
            }
            for feedback in all_feedback
        ]
        
        # Return response
        return make_response(jsonify(feedback_info), 200)
