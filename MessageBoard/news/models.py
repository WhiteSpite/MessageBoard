from django.db.models import *
from django.contrib.auth.models import User
from django.urls import reverse


def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'
   
   
class News(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='news')
    title = CharField(max_length=200)
    content = TextField()
    created_at = DateTimeField(auto_now_add=True)
    image = ImageField(upload_to=user_directory_path, null=True, blank=True)
    video = FileField(upload_to=user_directory_path, null=True, blank=True)
    
    def get_absolute_url(self):
        return reverse('news:post', kwargs={'pk': self.id})
