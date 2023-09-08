from celery import shared_task
from django.core.mail import send_mail as django_send_mail

@shared_task
def send_mail_to_admin(user, spec):
    django_send_mail('INFORMATION',
                     f'{user} has created a {spec}.',
                     'noreply@gmail.com',
                     ['admin@gmail.com'])

@shared_task
def send_mail_to_user(user_name, user_email, post_title, post_url):
    django_send_mail('INFORMATION',
                     f'Hi, {user_name}. You have a new comment on your post "{post_title}" (http://127.0.0.1:8000/{post_url}). '
                     f'It will be available to see after admin`s approve.',
                     'noreply@gmail.com',
                     [f'{user_email}']
                     )