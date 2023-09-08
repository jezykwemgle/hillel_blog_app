from celery import shared_task
from django.core.mail import send_mail as django_send_mail

@shared_task
def send_mail_to_admin(user, spec):
    django_send_mail('INFORMATION',
                     f'{user} has created {spec}.',
                     'noreply@gmail.com',
                     ['admin@gmail.com'])

@shared_task
def send_mail_to_user(user_name, user_email, post_title):
    django_send_mail('INFORMATION',
                     f'Hi, {user_name}. You have a new comment on your post "{post_title}"',
                     'noreply@gmail.com',
                     [f'{user_email}']
                     )