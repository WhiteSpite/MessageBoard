from django import template

register = template.Library()


@register.filter(name='get_parent_uri')
def get_parent_uri(value):
    return value[:-1][::-1].split('/', 1)[1][::-1]
