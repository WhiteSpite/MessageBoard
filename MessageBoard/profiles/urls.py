from django.urls import path
from .views import CodeVerificationView


app_name = 'profiles'
urlpatterns = [
    path('confirm-email/', CodeVerificationView.as_view(), name='code_verification'),
]
