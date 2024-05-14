import os, secrets
from datetime import timedelta


# Import the os module to interact with the operating system
import os

# Define the base directory as the absolute path of the directory of this file
basedir = os.path.abspath(os.path.dirname(__file__))

# Define a base configuration class
class Config():
    # Turn off debug mode by default
    DEBUG = False
    # Set the SQLite database directory to None by default
    SQLITE_DB_DIR = None
    # Set the SQLAlchemy database URI to None by default
    SQLALCHEMY_DATABASE_URI = None
    # Turn off SQLAlchemy's event system, which can consume a lot of resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Define a configuration class for local development
class LocalDev(Config):
    # Set the SQLite database directory to the db directory in the base directory
    SQLITE_DB_DIR = os.path.join(basedir, './db')
    # Set the SQLAlchemy database URI to the SQLite database in the db directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'db.sqlite3')  # Required for the application to work

    # Set the secret key for Flask-Security
    SECRET_KEY = 'your-secret-key'  
    # Set the password hash method for Flask-Security
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Required for the application to work
    # Set the password salt for Flask-Security
    SECURITY_PASSWORD_SALT = secrets.SystemRandom().getrandbits(128)  # Required for the application to work
    # Enable user registration in Flask-Security
    SECURITY_REGISTERABLE = True
    # Enable role joining in Flask-Security
    SECURITY_JOIN_USER_ROLES = True
    # Enable user tracking in Flask-Security
    SECURITY_TRACKABLE = True
    
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'authToken'
    
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 3

    # CSRF_ENABLED = True

    # Set the post-login view for Flask-Security
    SECURITY_POST_LOGIN_VIEW = '/logged_in'
    # Set the post-logout view for Flask-Security
    SECURITY_POST_LOGOUT_VIEW = '/bye'
    DEBUG = True


# Define a configuration class for production
class ProductionDev(Config):
    # Set the SQLite database directory to the db_directory in the parent of the base directory
    SQLITE_DB_DIR = os.path.join(basedir, '../db_directory')
    # Set the SQLAlchemy database URI to the SQLite database in the db_directory
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR, 'prod_db.sqlite3')  # Required for the application to work
    # Turn off debug mode for production
    DEBUG = False