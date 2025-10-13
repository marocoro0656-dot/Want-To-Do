
from django import template
register = template.Library()

@register.filter
def diff_row_class(diff):
    return {'high':'row-high','medium':'row-medium','low':'row-low'}.get(diff or 'low','row-low')

@register.filter
def diff_badge_class(diff):
    return {'high':'high','medium':'medium','low':'low'}.get(diff or 'low','low')
