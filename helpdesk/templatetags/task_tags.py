from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dict, key):
    return dict.get(key)

@register.filter
def get_filename(filename):
    return filename.split('/')[-1]




