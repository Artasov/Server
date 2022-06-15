from django import template
from APP_filehost.models import *

register = template.Library()


@register.simple_tag()
def diff(a, b, digits_after_dot=5, type_returned=1):
    if type_returned == 1:
        return float(str(a/b)[0:digits_after_dot])
    else:
        return int(float(str(a/b)[0:digits_after_dot]))
