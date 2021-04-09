from django import template

register = template.Library()

@register.filter(name='model_name')
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
