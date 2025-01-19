from django import template


register = template.Library()


@register.filter
def has_manager_perms(user):
    return user.groups.filter(name='manager').exists()