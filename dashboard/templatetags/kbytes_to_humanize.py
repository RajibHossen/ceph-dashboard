"""
django custom template tag for kilo bytes to gb format
"""
from django import template

register = template.Library()

@register.filter(name='kbytes_to_humanize')
def kbytes_to_humanize(bytes_value):
    """
    convert kbytes to mb/gb format
    :param bytes_value:
    :return:
    """
    try:
        return str("%.2f" % (float(bytes_value) / float(1024)))+" MB" # convert kb to MB
    except ValueError:
        return ''
