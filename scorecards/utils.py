from statistics import mean
from decimal import Decimal

from django.conf import settings


def bsc_rating(value):
    if value <= 80:
        return settings.BSC_RATING['very_poor']
    elif 80 < value < 100:
        return settings.BSC_RATING['poor']
    elif value == 100:
        return settings.BSC_RATING['average']
    elif 100 < value <= 120:
        return settings.BSC_RATING['good']
    elif value > 120:
        return settings.BSC_RATING['best']
    return 0


def get_bounds():
    average = Decimal(mean(settings.BSC_RATING.values()))
    lower = average - Decimal(0.5)
    upper = average + Decimal(0.5)
    return (lower, upper)


def get_inverse_contextual_rating(rating):
    """Returns context of rating to be used in template, either: success, warning, danger"""
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
    """Returns context of rating to be used in template, either: success, warning, danger"""
    bounds = get_bounds()
    if rating:
        if bounds[0] <= rating <= bounds[1]:
            return "warning"
        elif rating < bounds[0]:
            return "danger"
        else:
            return "success"
    return "default"
