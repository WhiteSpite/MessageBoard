from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    image = forms.ImageField(
        label='Изображение',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    video = forms.FileField(
        label='Видео',
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Announcement
        fields = ('title', 'content', 'category', 'image', 'video')
        labels = {
            'title': 'Заголовок*',
            'content': 'Содержание*',
            'category': 'Категория*',
            'image': 'Изображение',
            'video': 'Видео',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
