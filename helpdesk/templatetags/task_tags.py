from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter
def get_item(dict, key):
    return dict.get(key)

@register.filter
def get_filename(filename):
    return filename.split('/')[-1]

@register.filter
def get_fullname(username):
    full_name = username.split('.')
    full_name = '+'.join(full_name[0:2])
    return full_name


