from flask_sqlalchemy import *
from sqlalchemy.orm import validates, relationship, backref, contains_eager, subqueryload
from sqlalchemy.ext.mutable import MutableList
from flask_security import UserMixin, RoleMixin, AsaList
from datetime import datetime
from functools import wraps
from flask import request, jsonify
from flask import current_app
import os



db = SQLAlchemy()

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('User.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    permissions = db.Column(MutableList.as_mutable(AsaList()), nullable=True)

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    
    def __init__(self, email, password, active=True, roles=None, **kwargs):
        super().__init__(**kwargs)
        self.email = email
        self.password = password
        self.active = active

class BookRequest(db.Model):
    __tablename__ = 'book_request'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))  # Added book_id column
    status = db.Column(db.String(20), default='pending')

    book = db.relationship('Book', backref='requests')

class Section(db.Model):
    __tablename__ = 'section'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    description = db.Column(db.String())

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(255))
    content = db.Column(db.String(255))
    author = db.Column(db.String(255))
    status = db.Column(db.String(20), default='available')

    section = db.relationship('Section', backref='books')

class Issue(db.Model):
    __tablename__ = 'issue'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    issue_date = db.Column(db.DateTime, default=datetime.utcnow())
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='issued')

    user = relationship('User', backref='issues')
    book = relationship('Book', backref='issues')

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    feedback = db.Column(db.String(200))

class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    activity_timestamp = db.Column(db.DateTime, default=datetime.utcnow())
