from django.urls import path
from .views import *

app_name = 'news'
urlpatterns = [
    path('', NewsList.as_view(), name='posts'), 
    path('<int:pk>/', NewsDetail.as_view(), name='post'),
    path('add/', NewsAdd.as_view(), name='post_add'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('subscribe', subscribe, name='subscribe'),
    path('unsubscribe', unsubscribe, name='unsubscribe'),
]
