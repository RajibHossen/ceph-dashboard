from django import template

register = template.Library()

@register.filter(name='kbytes_to_humanize')
def percentage(bytes):
    try:
        return "%.2f" % (float(bytes) / float(1024)) # convert kb to MB
    except ValueError:
        return ''