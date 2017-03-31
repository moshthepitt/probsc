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
