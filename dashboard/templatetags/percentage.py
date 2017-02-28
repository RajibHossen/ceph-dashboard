from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(part,whole):
    try:
        return "%.2f" % ((float(part) / float(whole)) * 100.0)
    except ValueError:
        return ''

