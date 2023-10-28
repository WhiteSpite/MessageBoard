from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Response
from MessageBoard.settings import ALLOWED_HOSTS


@receiver(post_save, sender=Response)
def mail_post_owner(sender, instance, created, **kwargs):
    if created:
        subject = 'Новый отклик!'
        to_user = instance.announcement.user
        html_path = 'account/email/response_on_create.html'  
    else:
        subject = 'Отклик принят!'
        to_user = instance.user 
        html_path = 'account/email/response_on_accept.html'
        
    responder = instance.user
    post_title = instance.announcement.title
    post_id = instance.announcement.id
    response_text = instance.text
    post_url = f'http://{ALLOWED_HOSTS[0]}:8000{reverse("announcements:post", kwargs={"pk": post_id})}'
    if len(post_title) > 50:
        post_title = post_title[:50] + '...'
    html_content = render_to_string(html_path, 
        {'post_title': post_title,
            'post_url': post_url,
            'responder': responder, 
            'response_text': response_text})
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email='iliab02@yandex.ru',
        to=[to_user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()