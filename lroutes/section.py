from flask import current_app as app, jsonify, request, make_response
from db.models import *
from security_framework import current_user
from flask_restful import Resource
from flask_security import roles_accepted, auth_token_required, roles_required, auth_required

from datetime import datetime

class AllSections(Resource):
    @auth_required('token')
    def get(self):
        sections = Section.query.all()
        sections_info = [
            {
                'id': section.id,
                'name': section.name,
                'description': section.description,
                'date_created': section.date_created.strftime('%Y-%m-%d %H:%M:%S') if section.date_created else None
            }
            for section in sections
        ]
        return make_response(jsonify(sections_info), 200)

    @roles_accepted('admin','librarian')
    def post(self):
        data = request.get_json()
        name = data['name']
        description = data['description']
        try:
            section = Section(name=name, description=description, date_created=datetime.now())
            db.session.add(section)
            db.session.commit()

            return make_response(jsonify({'message': 'Section created successfully'}), 200)
        except Exception as e:
            return make_response(jsonify({'message': f'Some error occurred: {str(e)}'}), 400)


class SingleSection(Resource):
    @roles_accepted('admin','librarian')
    def patch(self, id):
        section = Section.query.get(id)
        if not section:
            return make_response(jsonify({'message': 'Section not found'}), 404)
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')

        if name is not None:
            section.name = name
        if description is not None:
            section.description = description

        db.session.commit()
        return make_response(jsonify({'message': 'Section updated successfully'}), 200)

    def get(self, id):
        section = Section.query.get(id)
        if section:
            section_info = {
                'id': section.id,
                'name': section.name,
                'description': section.description,
                'date_created': section.date_created.strftime('%Y-%m-%d %H:%M:%S') if section.date_created else None
            }
            return make_response(jsonify(section_info), 200)
        return make_response(jsonify({'message': 'Section not found'}), 404)

    @roles_accepted('admin','librarian')
    def delete(self, id):
        section = Section.query.get(id)
        if not section:
            return make_response(jsonify({'message': 'Section not found'}), 404)

        db.session.delete(section)
        db.session.commit()
        return make_response(jsonify({'message': 'Section deleted successfully'}), 200)

