from django import template

register = template.Library()

@register.filter(name='bytes_to_humanize')
def bytes_to_humanize(bytes):
    try:
        return str("%.2f" % (float(bytes) / float(1024*1024))) + ' MB' #convert bytes to MB
    except ValueError:
        return ''