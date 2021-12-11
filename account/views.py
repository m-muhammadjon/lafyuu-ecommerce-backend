from django.core.mail import send_mail

from .models import User, Verification


def email_sender(user_id):
    user = User.objects.get(id=user_id)
    token = Verification.objects.filter(user_id=user_id).first().token
    link = f'http://127.0.0.1:8000/verify/?token={token}'
    send_mail('Verify Account',
              f"Your verification link: {link}",
              'qqq155769@gmail.com',
              [user.email])

    return True
