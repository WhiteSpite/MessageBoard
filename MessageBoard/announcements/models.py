from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse


categories = [
    ('tanks', 'Танки'),
    ('healers', 'Хилы'),
    ('dd', 'ДД'),
    ('traders', 'Торговцы'),
    ('gildmasters', 'Гилдмастеры'),
    ('questgivers', 'Квестгиверы'),
    ('smiths', 'Кузнецы'),
    ('tanners', 'Кожевники'),
    ('potionmasters', 'Зельевары'),
    ('mages', 'Мастера заклинаний'),
]


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'


class Announcement(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='announcements')
    title = CharField(max_length=200)
    content = TextField()
    category = CharField(max_length=30, choices=categories)
    created_at = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to=user_directory_path, null=True, blank=True)
    video = FileField(upload_to=user_directory_path, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('announcements:post', kwargs={'pk': self.id})
    


class Response(Model):
    announcement = ForeignKey(
        Announcement, on_delete=CASCADE, related_name='responses')
    user = ForeignKey(User, on_delete=CASCADE, related_name='responses')
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)
    is_accepted = BooleanField(default=False)
    