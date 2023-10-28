from django.shortcuts import redirect
from django.views.generic import TemplateView
from .models import ConfirmationCode


class CodeVerificationView(TemplateView):
    template_name = "account/verification_sent.html" 
    
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        filter_res = ConfirmationCode.objects.filter(code=code)
        if filter_res.exists():
            activate_url = filter_res.first().activate_url
            filter_res.delete()
            return redirect(activate_url)
        else: 
            return redirect('profiles:code_verification')
    
