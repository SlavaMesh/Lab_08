from celery import shared_task
import datetime
from .models import Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@shared_task
def send_mail(users_mails: list):
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)

    html_content = render_to_string(
        template_name='daily_post.html',
        context={
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Статьи за неделю: {last_week}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=users_mails,
    )

    msg.attach_alternative(html_content, 'html/text')
