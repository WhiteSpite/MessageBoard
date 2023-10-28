import django_filters
from django import forms
from .models import News


class NewsFilter(django_filters.FilterSet):
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
    created_at = django_filters.DateFilter(
        label='',
        field_name='created_at',
        lookup_expr='icontains',
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Дата'}),
    )
    
    class Meta:
        model = News
        fields = [ 
            'title', 
            'content',
            'created_at'
        ]

