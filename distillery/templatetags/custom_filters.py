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
def replace_underscore(value):
    """Replace underscores with spaces in string."""
    if not value:
        return value
    return str(value).replace('_', ' ')
