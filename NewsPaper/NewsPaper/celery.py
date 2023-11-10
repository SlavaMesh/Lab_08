# import os
# from celery import Celery
# from celery.schedules import crontab
# from news.models import User
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
#
# app = Celery('NewsPaper')
# app.config_from_object('django.conf:settings', namespace='CELERY')
#
# app.autodiscover_tasks()
#
# # creating periodic task schedule
#
# users = User.objects.all()
# USERS_EMAILS = [u.email for u in users]
#
# app.conf.beat_schedule = {
#     'send_mail_on_new_posts_every_week_at_8_am': {
#         'task': 'news.task.send_mail',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#         'args': USERS_EMAILS,
#     }
# }
