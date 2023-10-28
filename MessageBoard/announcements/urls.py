from django.urls import path
from .views import *


app_name = 'announcements'
urlpatterns = [
    path('', AnnouncementList.as_view(), name='posts'),
    path('mine/', MyAnnouncementList.as_view(), name='my_posts'),
    path('<int:pk>/', AnnouncementDetail.as_view(), name='post'),
    path('add/', AnnouncementAdd.as_view(), name='post_add'),
    path('<int:pk>/edit/', AnnouncementEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', AnnouncementDelete.as_view(), name='post_delete'),
    path('responses/', ResponseList.as_view(), name='responses'),
    path('remove_response', remove_response, name='remove_response'),
    path('accept_response', accept_response, name='accept_response'),
    path('remove_all_responses_by_post', remove_all_responses_by_post, name='remove_all_responses_by_post'),
    path('remove_all_responses', remove_all_responses, name='remove_all_responses'),
    path('subscribe', subscribe, name='subscribe'),
    path('unsubscribe', unsubscribe, name='unsubscribe'),
]
