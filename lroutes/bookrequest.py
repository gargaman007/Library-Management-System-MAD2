from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import current_user
from flask_restful import Resource
from flask_security import roles_accepted, auth_token_required, roles_required, auth_required
from datetime import datetime
from datetime import timedelta



class UserBookRequests(Resource):
    @roles_accepted('user')
    @auth_required('token')
    def post(self):
        data = request.get_json()
        user_id = current_user.id
        book_id = data.get('book_id')

        # Check if the user exists
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        # Check if the user has reached the maximum allowed issues
        active_issues_count = Issue.query.filter_by(user_id=user_id).filter(Issue.due_date >= datetime.now()).count()
        if active_issues_count >= 5:
            return make_response(jsonify({'message': 'Maximum allowed active issues reached for the user'}), 400)

        # Check if the book exists and is available
        book = Book.query.filter_by(id=book_id, status='available').first()
        if not book:
            return make_response(jsonify({'message': 'Book not found or not available for request'}), 404)

        try:
            # Create a new book request
            book_request = BookRequest(user_id=user_id, book_id=book_id, status='pending')
            db.session.add(book_request)
            db.session.commit()

            return make_response(jsonify({'message': 'Book request created successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Error occurred: {str(e)}'}), 400)

class UpdateBookRequestStatus(Resource):
    @roles_accepted('librarian', 'admin')
    @auth_required('token')
    def patch(self, request_id):
        # Get the new status from the request JSON
        data = request.get_json()
        new_status = data.get('status')

        # Find the book request by ID
        book_request = BookRequest.query.get(request_id)

        if not book_request:
            return {'message': 'Book request not found'}, 404

        # Update the status and create an issue if the request is accepted
        if new_status == 'accepted':
            # Create a new issue
            due_date = datetime.now() + timedelta(days=7)
            new_issue = Issue(user_id=book_request.user_id, book_id=book_request.book_id, due_date=due_date, status='issued')
            db.session.add(new_issue)
        
        # Update the status of the book to 'not available'
            book = Book.query.get(book_request.book_id)
            if book:
                book.status = 'not available'
                db.session.commit()
            else:
                return {'message': 'Book not found'}, 404

        # Update the status of the book request
        book_request.status = new_status
        db.session.commit()

        return {'message': 'Book request status updated successfully'}, 200
    
class AllBookRequests(Resource):
    @roles_accepted('librarian', 'admin')
    @auth_required('token')
    def get(self):
        try:
            # Fetch all book requests
            book_requests = BookRequest.query.all()

            # Serialize the book requests data
            serialized_requests = [{
                'id': request.id,
                'user_id': request.user_id,
                'book_id': request.book_id,
                'status': request.status
            } for request in book_requests]

            return make_response(jsonify(serialized_requests), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Error occurred: {str(e)}'}), 400)
