from django import template

register = template.Library()

@register.filter(name='kbytes_to_humanize')
def kbytes_to_humanize(bytes):
    try:
        return str("%.2f" % (float(bytes) / float(1024)))+" MB" # convert kb to MB
    except ValueError:
        return ''