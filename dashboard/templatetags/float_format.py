"""
Django custom template tags
"""
from django import template

register = template.Library()

@register.filter(name='float_format')
def float_format(data):
    """
    format floting point value to two digit after decimel
    :param data:
    :return:
    """
    try:
        return "%.2f" % (float(data)) #return 2 digit after decimel
    except ValueError:
        return ''
