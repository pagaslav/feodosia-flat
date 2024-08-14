from django import template
from django.utils.safestring import SafeString, mark_safe

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': arg})
    return value

@register.filter(name='add_attribute')
def add_attribute(value, arg):
    if hasattr(value, 'as_widget'):
        attr, val = arg.split(':')
        return value.as_widget(attrs={attr: val})
    return value