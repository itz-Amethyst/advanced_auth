import random
from django.core.mail import EmailMessage

from account.models import User, OneTimePassword
from Advanced_Auth.settings import env


def generateOTP():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    Subject = "One time passcode for Email verification"
    otp_code = generateOTP()
    print(otp_code)
    user = User.objects.get(email = email)
    current_site = env("CURRENT_SITE")
    email_body = f"Hi {user.username} thanks for choosing us **{current_site} \n your OneTimePasscode is: {otp_code}"
    from_email = env("FROM_EMAIL")
    # settings.FROM_EMAIL
    OneTimePassword.objects.create(user = user, code = otp_code)

    d_email = EmailMessage(subject = Subject, body = email_body, from_email= from_email, to = [email])
    d_email.send(fail_silently = True)