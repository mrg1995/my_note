from celery import task
import time
from django.conf import settings
from django.core.mail import send_mail


@task
def send_Mail(token,email_to):
    msg = '<a href="http://127.0.0.1:8000/check/{}">点击激活</a>'.format(token)
    send_mail('注册激活','',settings.EMAIL_FROM,email_to,html_message=msg)
















