from django import template

register = template.Library()


@register.filter(name='verbose_name')
def get_verbose_name(object):
    return object._meta.verbose_name


@register.filter(name='verbose_name_plural')
def get_verbose_name_plural(object):
    return object._meta.verbose_name_plural
