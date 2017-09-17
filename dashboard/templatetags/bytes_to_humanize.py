"""
Custom template for django bytes to MB/GB conversion
"""
from django import template

register = template.Library()

@register.filter(name='bytes_to_humanize')
def bytes_to_humanize(byte_value):
    """
    convert bytes to mb/gb
    :param bytes:
    :return:
    """
    try:
        return str("%.2f" % (float(byte_value) / float(1024*1024))) + ' MB' #convert bytes to MB
    except ValueError:
        return ''
