from django import template

register = template.Library()

@register.filter(name='bytes_to_humanize')
def percentage(bytes):
    try:
        return "%.2f" % (float(bytes) / float(1024*1024)) #convert bytes to MB
    except ValueError:
        return ''