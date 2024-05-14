from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import roles_accepted, current_user, auth_token_required
from flask_restful import Resource
from .cache import cache

class AllIssues(Resource):
    @roles_accepted('admin', 'librarian', 'user')
    @auth_token_required
    # @cache.cached(timeout=50)
    def get(self):
        issues = Issue.query.all()
        issues_info = [
            {
                'id': issue.id,
                'user_id': issue.user_id,
                'book_id': issue.book_id,
                'issue_date': issue.issue_date,
                'due_date': issue.due_date,
                'status': issue.status  # Include status in the response
            }
            for issue in issues
        ]
        return make_response(jsonify(issues_info), 200)

    @roles_accepted('admin', 'librarian')
    @auth_token_required
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        book_id = data.get('book_id')
        issue_date = data.get('issue_date')
        due_date = data.get('due_date')
        status = data.get('status', 'issued')  # Default to 'issued' if not provided

        try:
            issue = Issue(
                user_id=user_id,
                book_id=book_id,
                issue_date=issue_date,
                due_date=due_date,
                status=status
            )
            db.session.add(issue)
            db.session.commit()

            return make_response(jsonify({'message': 'Issue created successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Some error occurred: {str(e)}'}), 400)
        
class UserIssues(Resource):
    @auth_token_required
    def get(self):
        user_id = current_user.id  # Get the ID of the current user

        # Query all issues related to the current user
        issues = Issue.query.filter_by(user_id=user_id).all()

        # Construct issue information for response
        issues_info = []
        for issue in issues:
            # Fetch the book information for the current issue
            book = Book.query.get(issue.book_id)
            if book:
                issue_info = {
                    'id': issue.id,
                    'user_id': issue.user_id,
                    'book_id': issue.book_id,
                    'book_content': book.content,
                    'issue_date': issue.issue_date,
                    'due_date': issue.due_date,
                    'status': issue.status
                }
                issues_info.append(issue_info)

        return make_response(jsonify(issues_info), 200)

class SingleIssue(Resource):

    @roles_accepted('admin', 'librarian', 'user')  # Allow users to update and return books
    @auth_token_required
    def patch(self, id):
        issue = Issue.query.get(id)
        if not issue:
            return make_response(jsonify({'message': 'Issue not found'}), 404)

        data = request.get_json()
        user_id = data.get('user_id')
        book_id = data.get('book_id')
        issue_date = data.get('issue_date')
        due_date = data.get('due_date')
        status = data.get('status')

        # Update issue fields if provided
        if user_id is not None:
            issue.user_id = user_id
        if book_id is not None:
            issue.book_id = book_id
        if issue_date is not None:
            issue.issue_date = issue_date
        if due_date is not None:
            issue.due_date = due_date
        if status is not None:
            # If status is 'returned', update issue and book status
            if status == 'returned':
                issue.status = status
                issue.return_date = datetime.utcnow()
                book = Book.query.get(issue.book_id)
                if book:
                    book.status = 'available'
            else:
                issue.status = status

        try:
            db.session.commit()
            return make_response(jsonify({'message': 'Issue updated successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Some error occurred: {str(e)}'}), 400)


    @roles_accepted('admin', 'librarian')
    @auth_token_required
    def get(self, id):
        issue = Issue.query.get(id)
        if issue:
            issue_info = {
                'id': issue.id,
                'user_id': issue.user_id,
                'book_id': issue.book_id,
                'issue_date': issue.issue_date,
                'due_date': issue.due_date,
                'status': issue.status  # Include status in the response
            }
            return make_response(jsonify(issue_info), 200)
        return make_response(jsonify({'message': 'Issue not found'}), 404)

    @roles_accepted('admin', 'librarian')
    @auth_token_required
    def delete(self, id):
        issue = Issue.query.get(id)
        if not issue:
            return make_response(jsonify({'message': 'Issue not found'}), 404)

        db.session.delete(issue)
        db.session.commit()
        return make_response(jsonify({'message': 'Issue deleted successfully'}), 200)