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
    full_name = username.split('@')
    full_name = full_name[0].split('.')
    full_name = [x.capitalize() for x in full_name]
    return full_name

@register.filter
def join_name_surname(full_name):
    joined_names = '+'.join(full_name)
    return joined_names

