"""
Django custom template tags for showing percentage value
"""
from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(part, whole):
    """
    convert to percentage and return
    :param part:
    :param whole:
    :return:
    """
    try:
        return "%.2f" % ((float(part) / float(whole)) * 100.0)
    except ValueError:
        return ''

