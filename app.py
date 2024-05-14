import os
from flask import Flask, send_from_directory
from flask_restful import Api
from jinja2 import Template

from config import LocalDev
from flask import render_template_string

from security_framework import security, user_datastore, roles_required, current_user
from db.models import db, User

from functools import wraps

from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import func


from flask_mail import Mail, Message
from celery import Celery
from celery.schedules import crontab
from db.models import *

from lroutes.cache import cache
from lroutes.mailservice import send_message

# Initialize the app variable to None
app = None
api = None

# Define the create_app function
def create_app():
    # Create an instance of the Flask class
    app = Flask(__name__)
    # Configure the app using the LocalDev class
    app.config.from_object(LocalDev)
    
    # Initialize the db object with the app
    db.init_app(app)
    # Push an application context onto the stack
    app.app_context().push()
    print('Database initialized')

    api = Api(app)
    cache.init_app(app)
    app.app_context().push()
    print('API initialized')

    print('App setup complete.')
    # Return the app
    return app, api
    
# Call the create_app function and assign the result to the app variable
app, api_handler = create_app()

# Initialize the security object with the app and the user_datastore
security.init_app(app, user_datastore)

CORS(app)



celery=Celery(app.name,broker='redis://localhost:6379/1',backend='redis://localhost:6379/2')







from lroutes.auth import *
api_handler.add_resource(login, '/api/login')
api_handler.add_resource(logout, '/api/logout')
api_handler.add_resource(register, '/api/register')

from lroutes.section import *
api_handler.add_resource(AllSections, '/api/section')
api_handler.add_resource(SingleSection, '/api/section/<int:id>')

from lroutes.books import *

# Routes for managing books in a section
api_handler.add_resource(AllBooksInSection, '/api/section/<int:section_id>/books')
api_handler.add_resource(SingleBookInSection, '/api/section/<int:section_id>/book/<int:book_id>')
api_handler.add_resource(CRUDBookInSection, '/api/section/<int:section_id>/book/<int:book_id>')

# Routes for managing all books
api_handler.add_resource(AllBooks, '/api/books')
api_handler.add_resource(NewBook, '/api/book/<int:section_id>')
api_handler.add_resource(UpdateBook, '/api/book/<int:book_id>')
api_handler.add_resource(GetBook, '/api/book/<int:book_id>')




from lroutes.issue import *
api_handler.add_resource(AllIssues, '/api/issues')
api_handler.add_resource(SingleIssue, '/api/issues/<int:id>')
api_handler.add_resource(UserIssues,'/api/userissues')


from lroutes.search import *
api_handler.add_resource(LibrarySearch, '/api/books/search')

from lroutes.admin import *
api_handler.add_resource(AdminDashboard, '/api/admin-dashboard')
api_handler.add_resource(Export, '/api/export/<string:export_type>')

from lroutes.feedback import *
api_handler.add_resource(FeedbackResource, '/api/feedback')
api_handler.add_resource(AllFeedbackResource, '/api/all-feedback')  

from lroutes.user_profile import *
api_handler.add_resource(UserProfileResource,'/api/profile')

from lroutes.bookrequest import *
api_handler.add_resource(UserBookRequests, '/api/bookrequest')
api_handler.add_resource(UpdateBookRequestStatus, '/api/update-book-request/<int:request_id>')
api_handler.add_resource(AllBookRequests, '/api/all-book-requests')


# Define the Celery task
@celery.task
def check_due_date():
    # Get current date
    current_date = datetime.utcnow()
    # Query for all issued books whose due date has passed
    overdue_issues = Issue.query.filter(Issue.due_date < current_date, Issue.status == 'issued').all()
    # Update the status of each issue and the corresponding book
    for issue in overdue_issues:
        issue.status = 'returned'
        issue.book.status = 'available'
    # Commit changes to the database
    db.session.commit()
    
# Define the Celery task
@celery.task
def send_login_reminder():
    # Get the current date and time
    current_datetime = datetime.utcnow()
    # Calculate the threshold date for last login (1 day ago)
    threshold_datetime = current_datetime - timedelta(days=1)
    # Query for users whose last login was more than 1 day ago
    inactive_users = User.query.filter(User.current_login_at < threshold_datetime).all()
    # Send a reminder email to each inactive user
    for user in inactive_users:
        send_message(user.email, 'Login Reminder', 'Please log in to your account to stay updated.')

        
def generate_monthly_report():
    # Get the current date and time
    current_date = datetime.utcnow()
    # Calculate the start and end date for the previous month
    start_date = datetime(current_date.year, current_date.month - 1, 1)
    end_date = datetime(current_date.year, current_date.month, 1) - timedelta(days=1)
    
    # Query to get total books
    total_books = Book.query.count()
    
    # Query to get total sections
    total_sections = Section.query.count()
    
    # Query to get the number of users
    total_users = User.query.count()
    
    # Query to get all feedback received in the previous month
    feedback_received = Feedback.query.all()

    # Render the HTML template with the summary statistics and feedback
    with open('templates/monthly_report.html', 'r') as f:
        template = Template(f.read())
    html_content = template.render(
        total_books=total_books,
        total_sections=total_sections,
        total_users=total_users,
        feedback_received=feedback_received
    )

    return html_content

@celery.task
def send_monthly_report():
    # Get the admin email address
    admin_email = 'admin@gmail.com'
    
    # Generate the monthly report
    monthly_report = generate_monthly_report()

    # Send the report as an email to the admin email address
    send_message(admin_email, 'Monthly Summary Report', monthly_report)


# Schedule the task to run periodically
celery.conf.beat_schedule = {
    'check-due-date': {
        'task': 'app.check_due_date',
        'schedule': crontab(minute=33, hour=16),  # Run every 24 hours
    },
        'send-login-reminder': {
        'task': 'app.send_login_reminder',
        'schedule': crontab(minute=33, hour=16),  # Run every 24 hours
    },
        'send-monthly-report': {
        'task': 'app.send_monthly_report',
        'schedule': crontab(minute=33, hour=16),  # Run on the first day of the month at midnight
    }
}

     


           


if __name__ == '__main__': 
    app.run()