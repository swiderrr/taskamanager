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

@register.filter
def text_to_hexcolor(full_name):
    full_name = ''.join(full_name)
    hex = []
    slice = full_name[:6]
    ascii_list = [ord(x) for x in slice]
    for char in ascii_list:
        num = ((char / 16) - (char // 16)) * 16
        hex.append(int(num))
    hex = [repr(i) for i in hex]
    color = list(''.join(hex))
    color = ''.join(color[:6])
    return color

