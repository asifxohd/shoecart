# user_home/signals.py

from django.dispatch import Signal
from django.core.mail import send_mail

# your signals.py code goes here

contact_form_submitted = Signal()

def send_email_and_respond(sender, **kwargs):
    email = kwargs.get('email')
    message = kwargs.get('message')

    try:
        # Send the email
        send_mail('Contact Form Submission', message, email, ['shoecartcalicut@gmail.com'])
        # Send a response email to the user
        send_mail('Thank you for contacting us', 'We will get back to you.', 'your@email.com', [email])
        
        # Respond with a success message
        # You can customize the response as needed
        print('Form submitted successfully')
    except Exception as e:
        # Handle email sending errors
        print('Failed to send the email')

# Connect the signal handler function to the custom signal
contact_form_submitted.connect(send_email_and_respond)
