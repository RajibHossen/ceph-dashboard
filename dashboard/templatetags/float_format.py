from django import template

register = template.Library()

@register.filter(name='float_format')
def float_format(data):
    try:
        return "%.2f" % (float(data)) #return 2 digit after decimel
    except ValueError:
        return ''