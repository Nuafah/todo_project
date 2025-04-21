from django import template
register = template.Library()

@register.filter
def get_status(queryset, status):
    return queryset.filter(status=status)
