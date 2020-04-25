from bestbid.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from celery import Celery, shared_task
from time import sleep

# app = Celery('tasks', broker='amqp://admin:admin@localhost:5672/myvhost')
# app = Celery('tasks', broker='amqp://127.0.0.1:5672')

@shared_task
def send_email_task():
	sleep(10)
	subject = "Celery Test"
	message = "<h2>Sent with celery</h2>"
	send_mail(subject, message, EMAIL_HOST_USER, ['eebfxywrqmkrzspccn@ttirv.com'], fail_silently=False)
	return None