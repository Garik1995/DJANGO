from django import template

register = template.Library ()


@register.filter
def total(price, count):
    return price * count
