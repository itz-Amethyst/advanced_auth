from django.conf import settings
from django.core.mail import EmailMessage


def send_email(data):
    email = EmailMessage(
        subject = data['email_subject'],
        body = data['email_body'],
        to = [data['to_email']],
        from_email = settings.EMAIL_HOST
    )

    email.send()