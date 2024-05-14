from flask import jsonify, make_response, send_file
from flask_restful import Resource
from db.models import Book, Section, Issue, Feedback, UserActivity, db
import csv
from io import StringIO
from sqlalchemy import func
from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import current_user
from flask_restful import Resource
from flask_security import roles_accepted, auth_token_required, roles_required, auth_required
from datetime import datetime
from datetime import timedelta

class AdminDashboard(Resource):
    @roles_accepted('librarian', 'admin')
    def get(self):
        # Calculate issue quantity
        issue_quantity = db.session.query(func.count(Issue.id)).scalar()

        # Calculate number of books available
        available_books = db.session.query(func.count(Book.id)).filter_by(status='available').scalar()

        # Calculate total number of books
        total_books = db.session.query(func.count(Book.id)).scalar()

        # Calculate total categories
        total_categories = db.session.query(func.count(Section.id)).scalar()

        # Prepare JSON response
        response_data = {
            'issueQuantity': issue_quantity,
            'availableBooks': available_books,
            'totalBooks': total_books,
            'totalCategories': total_categories
        }

        return jsonify(response_data)

class Export(Resource):
    @roles_accepted('librarian', 'admin')
    def export_csv(self, data):
        return make_response(jsonify(data), 200)

    def get(self, export_type):
        if export_type == 'export-issues-csv':
            data = [(issue.id, issue.user_id, issue.book_id, issue.issue_date, issue.due_date, issue.status) for issue in Issue.query.all()]
        elif export_type == 'export-feedbacks-csv':
            data = [(feedback.id, feedback.issue_id, feedback.user_id, feedback.feedback) for feedback in Feedback.query.all()]
        elif export_type == 'export-user-activities-csv':
            data = [(activity.id, activity.user_id, activity.activity_type, activity.activity_timestamp) for activity in UserActivity.query.all()]
        elif export_type == 'export-books-csv':
            data = [(book.id, book.section_id, book.name, book.description, book.content, book.author, book.status) for book in Book.query.all()]
        elif export_type == 'export-sections-csv':
            data = [(section.id, section.name, section.date_created, section.description) for section in Section.query.all()]
        else:
            return make_response(jsonify({'error': 'Invalid export type'}), 400)

        return self.export_csv(data)

