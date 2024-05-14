from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import roles_accepted, current_user, auth_token_required
from flask_restful import Resource
from werkzeug.utils import secure_filename
import os
from .cache import cache



class AllBooksInSection(Resource):
    @cache.cached(timeout=10)
    def get(self, section_id):
        books = Book.query.filter_by(section_id=section_id).all()
        books_info = [
            {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'author': book.author,
                'description': book.description,
                'content': book.content,
                'status': book.status,
            }
            for book in books
        ]
        return make_response(jsonify(books_info), 200)

class SingleBookInSection(Resource):
    @cache.cached(timeout=10)
    def get(self, section_id, book_id):
        book = Book.query.filter_by(section_id=section_id, id=book_id).first()
        if book:
            book_info = {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'author': book.author,
                'description': book.description,
                'content': book.content,
                'status': book.status,
            }
            return make_response(jsonify(book_info), 200)
        return make_response(jsonify({'message': 'Book not found'}), 404)
    
class CRUDBookInSection(Resource):
    def get(self, section_id, book_id):
        book = Book.query.filter_by(section_id=section_id, id=book_id).first()
        if book:
            book_info = {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'author': book.author,
                'description': book.description,
                'content': book.content,
                'status': book.status,
            }
            return make_response(jsonify(book_info), 200)
        return make_response(jsonify({'message': 'Book not found'}), 404)

class GetBook(Resource):
    def get(self, book_id):
        book = Book.query.filter_by(id=book_id).first()
        if book:
            book_info = {
                'id': book.id,
                'section_id': book.section_id,
                'name': book.name,
                'author': book.author,
                'description': book.description,
                'content': book.content,
                'status': book.status,
            }
            return make_response(jsonify(book_info), 200)
        return make_response(jsonify({'message': 'Book not found'}), 404)

class AllBooks(Resource):
    # @cache.cached(timeout=50)
    def get(self):
        books = Book.query.all()
        books_info = [
            {
                'id': book.id,
                'section_name': book.section.name if book.section else '',  # Check if section exists
                'section_id': book.section_id if book.section else None,  # Check if section exists
                'name': book.name,
                'author': book.author,
                'description': book.description,
                'content': book.content,
                'status': book.status,
            }
            for book in books
        ]
        return make_response(jsonify(books_info), 200)

class NewBook(Resource):
    @roles_accepted('librarian', 'admin')
    def post(self, section_id):
        data = request.form
        name = data.get('name')
        author = data.get('author')
        description = data.get('description')
        content_url = data.get('content')  # Change to content_url



        try:
            book = Book(
                section_id=section_id,
                name=name,
                author=author,
                description=description,
                content=content_url,  # Save the content URL in the database
                status='available'
            )
            db.session.add(book)
            db.session.commit()

            return make_response(jsonify({'message': 'Book created successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Some error occurred: {str(e)}'}), 400)

class UpdateBook(Resource):
    @roles_accepted('librarian', 'admin')
    def patch(self, book_id):
        data = request.form
        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        book.name = data.get('name', book.name)
        book.author = data.get('author', book.author)
        book.section_id = data.get('section_id', book.section_id)
        
        book.description = data.get('description', book.description)
        book.content = data.get('content', book.content)  # Change to content_url

        try:
            db.session.commit()
            return make_response(jsonify({'message': 'Book updated successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Some error occurred: {str(e)}'}), 400)

    @roles_accepted('librarian', 'admin')
    def delete(self, book_id):
        book = Book.query.filter_by(id=book_id).first()

        if not book:
            return make_response(jsonify({'message': 'Book not found'}), 404)

        try:
            db.session.delete(book)
            db.session.commit()
            return make_response(jsonify({'message': 'Book deleted successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Some error occurred: {str(e)}'}), 400)

