# Flask imports
from app import app
from flask import render_template

# SendGrid API
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(subject, sender, recipients, body):      # SendGrid API - Create and Send email
    message = Mail(
        from_email=sender,          # Sender
        to_emails=recipients,       # Receiver
        subject=subject,            # Subject
        html_content=body           # Body
    )
    sg = SendGridAPIClient(app.config['MAIL_PASSWORD'])     # SendGrid API Authenticator
    response = sg.send(message)                             # Send Email

def send_password_reset_email(user):                            # Create and Email a Password Reset Token to a logged-in user
    token = user.get_reset_password_token()                     # Create a token for the logged-in user
    send_email('[MIRC Data Dashboard] Reset Your Password',     # Email the token
               sender=app.config['MAIL_DEFAULT_SENDER'],        # Sender
               recipients=[user.email],                         # Receiver
               body=render_template(
                   'email/reset_password.html',                 # HTML template
                   user=user,                                   # Logged-in user
                   token=token                                  # Create token
                )
            )