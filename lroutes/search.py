from flask import request, make_response, jsonify
from flask_restful import Resource
from sqlalchemy import or_
from db.models import *
from security_framework import roles_accepted, current_user, auth_token_required

class LibrarySearch(Resource):
    def get(self):
        query = request.args.get('query', '').lower()

        book_results = db.session.query(Book, Section).\
            join(Section, Section.id == Book.section_id).\
            filter(
                or_(
                    db.func.lower(Book.name).contains(query),
                    db.func.lower(Book.description).contains(query),
                    db.func.lower(Section.name).contains(query)
                )
            ).all()

        search_results = [
            {
                'book_id': book.id,
                'section_id': book.section_id,
                'book_name': book.name,
                'description': book.description,
                'content': book.content,
                'author': book.author,
                'section_name': section.name,
            }
            for book, section in book_results
        ]

        return make_response(jsonify(search_results), 200)
