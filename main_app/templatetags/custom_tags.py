from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='ingredient_linebreaks')
def ingredient_linebreaks(value):
    return mark_safe(value.replace('\r\n', '</li><li>'))