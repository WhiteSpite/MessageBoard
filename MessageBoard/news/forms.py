from django import forms
from .models import News


class NewsForm(forms.ModelForm):
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
        model = News
        fields = ('title', 'content', 'image', 'video')
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
        }