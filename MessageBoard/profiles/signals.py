from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Profile
from news.models import News
from announcements.models import Announcement
from MessageBoard.settings import ALLOWED_HOSTS


def mailing(sender, instance):
    if sender == News:
        subject = 'Новая новость на портале!'
        profiles = Profile.objects.filter(subscribed_to_news=True)
        app_name = 'news'
    elif sender == Announcement:
        subject = 'Новое объявление на портале!'
        profiles = Profile.objects.filter(subscribed_to_announcements=True)
        app_name = 'announcements'

    if not profiles.exists():
        return
    html_path = 'account/email/mailing_post_on_create.html'
    post_title = instance.title
    post_id = instance.id
    post_user = instance.user
    post_content = instance.content
    post_url = f'http://{ALLOWED_HOSTS[0]}:8000{reverse(f"{app_name}:post", kwargs={"pk": post_id})}'
    if len(post_title) > 50:
        post_title = post_title[:50] + '...'
    html_content = render_to_string(html_path,
        {'post_title': post_title,
            'post_user': post_user,
            'post_url': post_url,
            'post_content': post_content})
    for profile in profiles:
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email='iliab02@yandex.ru',
            to=[profile.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=News)
def mailing_news_on_create(sender, instance, created, **kwargs):
    if created:
        mailing(sender, instance)


@receiver(post_save, sender=Announcement)
def mailing_announcement_on_create(sender, instance, created, **kwargs):
    if created:
        mailing(sender, instance)
