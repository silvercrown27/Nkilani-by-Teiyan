from django import template

register = template.Library()


@register.filter(name='get_stars')
def get_stars(reviews, rating):
    return range(rating)


@register.filter(name='get_empty_stars')
def get_empty_stars(reviews, rating):
    return range(5 - rating)
