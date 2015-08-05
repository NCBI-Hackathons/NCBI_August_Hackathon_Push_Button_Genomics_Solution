from django import template

register = template.Library()

@register.filter
def get_or_none(o, k):
    if o:
        if k in o:
            return o[k]
    return None
