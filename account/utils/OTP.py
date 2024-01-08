import random
from django.core.mail import EmailMessage

from account.models import User, OneTimePassword
from django.conf import settings
from Advanced_Auth.settings import env


# Todo use pyotp package to implement expire for it also use cookie to save info in page if user forgot the otp code on email inbox it would be accessible to recover it with another api send verify email again
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
    from_email = settings.EMAIL_HOST
    # settings.FROM_EMAIL
    OneTimePassword.objects.create(user = user, code = otp_code)

    d_email = EmailMessage(subject = Subject, body = email_body, from_email= from_email, to = [email])
    d_email.send(fail_silently = True)