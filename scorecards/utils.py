from statistics import mean
from decimal import Decimal

from django.conf import settings


def bsc_rating(value, customer=None):
    bsc_rating_dict = settings.BSC_RATING
    if customer:
        bsc_rating_dict = customer.get_bsc_rating_dict()
    if value <= 80:
        return Decimal(bsc_rating_dict['very_poor'])
    elif 80 < value < 100:
        return Decimal(bsc_rating_dict['poor'])
    elif value == 100:
        return Decimal(bsc_rating_dict['average'])
    elif 100 < value <= 120:
        return Decimal(bsc_rating_dict['good'])
    elif value > 120:
        return Decimal(bsc_rating_dict['best'])
    return Decimal(0)


def get_bounds():
    average = Decimal(mean(settings.BSC_RATING.values()))
    lower = average - Decimal(0.5)
    upper = average + Decimal(0.5)
    return (lower, upper)


def get_inverse_contextual_rating(rating):
    """Returns context of rating to be used in template, either: success,
    warning, danger"""
    bounds = get_bounds()
    if rating:
        if bounds[0] <= rating <= bounds[1]:
            return "warning"
        elif rating > bounds[0]:
            return "danger"
        else:
            return "success"
    return "default"


def get_contextual_rating(rating):
    """Returns context of rating to be used in template, either: success,
    warning, danger"""
    bounds = get_bounds()
    if rating:
        if bounds[0] <= rating <= bounds[1]:
            return "warning"
        elif rating < bounds[0]:
            return "danger"
        else:
            return "success"
    return "default"


def get_contextual_color(rating):
    bounds = get_bounds()
    if rating:
        if bounds[0] <= rating <= bounds[1]:
            return settings.BSC_COLOR_WARN
        elif rating < bounds[0]:
            return settings.BSC_COLOR_BAD
        else:
            return settings.BSC_COLOR_GOOD
    return "#d9edf7"


def get_inverse_contextual_color(rating):
    bounds = get_bounds()
    if rating:
        if bounds[0] <= rating <= bounds[1]:
            return settings.BSC_COLOR_WARN
        elif rating > bounds[0]:
            return settings.BSC_COLOR_BAD
        else:
            return settings.BSC_COLOR_GOOD
    return "#d9edf7"
