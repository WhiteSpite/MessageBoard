import django_filters
from django import forms
from .models import Announcement, categories, Response


class AnnouncementFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(
        label='', 
        field_name='user__username', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Игрок'}),
        lookup_expr='icontains')
    title = django_filters.CharFilter(
        label='', 
        field_name='title', 
        lookup_expr='icontains', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}))
    content = django_filters.CharFilter(
        label='', 
        field_name='content', 
        lookup_expr='icontains', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Содержание'}))
    category = django_filters.ChoiceFilter(
        field_name='category',
        empty_label='Выберите категорию',
        choices=categories,
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}))
        
    
    class Meta:
        model = Announcement
        fields = [
            'user', 
            'title', 
            'content',
            'category',
        ]
        

class MyAnnouncementFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        label='', 
        field_name='title', 
        lookup_expr='icontains', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}))
    content = django_filters.CharFilter(
        label='', 
        field_name='content', 
        lookup_expr='icontains', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Содержание'}))
    category = django_filters.ChoiceFilter(
        field_name='category',
        choices=categories,
        empty_label='Выберите категорию',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Announcement
        fields = [ 
            'title', 
            'content',
            'category',
        ]


class ResponseFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        current_username = kwargs.pop('current_username')
        super().__init__(*args, **kwargs) 
        self.filters['announcement'] = django_filters.ModelChoiceFilter(
            field_name='announcement',
            queryset=Announcement.objects.filter(user__username=current_username),
            empty_label='Выберите объявление',
            label='',
            widget=forms.Select(attrs={'class': 'form-control form-field', 'placeholder': 'Объявление'}),)
        
    user = django_filters.CharFilter(
        label='', 
        field_name='user__username', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Игрок'}),
        lookup_expr='icontains')
    announcement__category = django_filters.ChoiceFilter(
        field_name='announcement__category',
        choices=categories,
        empty_label='Выберите категорию',
        label='',
        widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Response
        fields = [
            'announcement', 
            'announcement__category', 
            'user',
        ]
        