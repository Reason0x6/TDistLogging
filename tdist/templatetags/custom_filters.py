from django import template

register = template.Library()

@register.filter
def get_field(obj, field_name):
    """Get a field value from an object by field name."""
    try:
        return getattr(obj, field_name)
    except AttributeError:
        return None

@register.filter
def replace(value, arg):
    """Replace substring in string."""
    if not value or not arg:
        return value
    old, new = arg.split(',') if ',' in arg else (arg, ' ')
    return str(value).replace(old, new)
