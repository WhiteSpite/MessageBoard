from django.core.mail import EmailMultiAlternatives
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.sites.shortcuts import get_current_site
from .models import ConfirmationCode


class CodeAccountAdapter(DefaultAccountAdapter):
    # def send_mail(self, template_prefix, email, context):
    #     code = ConfirmationCode.objects.create(user=context['user']).code
    #     msg = EmailMultiAlternatives(
    #         subject="Код подтверждения",
    #         body=f"Ваш код подтверждения: {code}",
    #         from_email="iliab02@yandex.ru",
    #         to=[email],
    #     )
    #     msg.send()

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        user = emailconfirmation.email_address.user
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        code_objects = ConfirmationCode.objects.filter(user=user)
        if code_objects.exists():
            code_objects.delete()
        code = ConfirmationCode.objects.create(user=user, activate_url=activate_url).code
        ctx = {
            "user": user,
            "code": code,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        self.send_mail(
            email_template, emailconfirmation.email_address.email, ctx)
