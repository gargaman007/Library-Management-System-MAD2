import os
from app import create_app
from security_framework import security, user_datastore, create_roles, admin_user_creation, librarian_user_creation

from db.models import *
from datetime import datetime


# Create an instance of the application
app, api = create_app()

# Use the application context to ensure that the database operations are performed in the right context
with app.app_context():
    try:
        # Drop all existing tables in the database
        db.drop_all()
        # Create all tables defined in the SQLAlchemy models
        db.create_all()
        # Commit the changes to the database
        db.session.commit()
        # Print a message to indicate that the tables have been created
        print('Database tables created')

        # Call the function to create roles
        create_roles()
        # Print a message to indicate that the roles have been added
        print('Roles added, ie admin, user')

        # Call the function to create the admin user
        if admin_user_creation():
            # Print a message to indicate that the admin user has been created
            print('Admin created')
        
        # Create librarian user
        if librarian_user_creation():
            print('Librarian Created')

        # Create Sample Categories
        section1 = Section(
            name='History', 
            description='History Section'
            )
        db.session.add(section1)
        section2 = Section(
            name='Mathematics',
            description='Mathematics Books'
            )
        db.session.add(section2)

        db.session.commit()

        # create 2 product
        book1 = Book(
            name='History Book',
            section_id=1, 
            description='description1',
            content='content',
            author='author'
        )
        db.session.add(book1)


        # Commit any changes to the database
        db.session.commit()
        


    except Exception as e:
        print(f"Error creating database tables: {e}")