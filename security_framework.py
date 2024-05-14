import bcrypt
from flask import jsonify, make_response
from flask_security import *
from db.models import db, User, Role, UserActivity
from werkzeug.security import *

# Create an instance of SQLAlchemyUserDatastore. This is a datastore for Flask-Security that uses SQLAlchemy.
# It provides an interface for Flask-Security to interact with the User and Role models.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Create an instance of Security. This is the main class for Flask-Security.
# It ties together the various components of Flask-Security for use in your application.
security = Security()


# Function to create roles
def create_roles():
    # Define roles and their permissions
    roles_permissions = {
        'admin': 'admin-access',
        'user': 'user-access',
        'librarian': 'librarian-access'
    }
    # Iterate over each role
    for role_name, role_permissions in roles_permissions.items():
        # Check if the role already exists
        role = Role.query.filter_by(name=role_name).first()
        # If the role does not exist, create it
        if not role:
            role = Role(name=role_name, description=role_permissions)
            # Add the new role to the session
            db.session.add(role)
    # Commit the session to save the changes
    db.session.commit()

def librarian_user_creation():
    # Get the librarian role
    librarian_role = Role.query.filter_by(name='librarian').first()
    # Check if there is already a user with the librarian role
    librarian_user = User.query.filter(User.roles.any(id=librarian_role.id)).first()

    # If there is no librarian user, create one
    if not librarian_user:
        # Define the librarian email and password
        librarian_email = 'librarian@gmail.com'
        librarian_password = 'librarian'
        # Hash the password
        hashed_password = bcrypt.hashpw(librarian_password.encode('utf-8'), bcrypt.gensalt())

        # Create the librarian user
        user_user = user_datastore.create_user(email=librarian_email, password=hashed_password)
        # Add the librarian role to the user
        user_datastore.add_role_to_user(user_user, 'librarian')
        # Commit the session to save the changes
        db.session.commit()
        return True
    return False


# Function to create an admin user
def admin_user_creation():
    # Get the admin role
    admin_role = Role.query.filter_by(name='admin').first()
    # Check if there is already a user with the admin role
    admin_user = User.query.filter(User.roles.any(id=admin_role.id)).first()

    # If there is no admin user, create one
    if not admin_user:
        # Define the admin email and password
        admin_email = 'admin@gmail.com'
        admin_password = 'admin'
        # Hash the password
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

        # Create the admin user
        user_user = user_datastore.create_user(email=admin_email, password=hashed_password)
        # Add the admin role to the user
        user_datastore.add_role_to_user(user_user, 'admin')
        # Commit the session to save the changes
        db.session.commit()
        return True
    return False

def admin_user_status_check():      #test
    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User.query.filter(User.roles.any(id=admin_role.id)).first()

    # If there is no admin user, create one
    if admin_user and admin_user.active == True and admin_user.email == 'abc@abc.com':
        return True
    return False

def login_function(email, password):
    user = user_datastore.find_user(email=email)

    if user :
        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            auth_token = user.get_auth_token()
            login_user(user)
            activity = UserActivity(user_id=user.id, activity_type='login')
            db.session.add(activity)
            db.session.commit()
            return True
    else:
        return False