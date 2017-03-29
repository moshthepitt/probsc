from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel


class KPI(TimeStampedModel):
    """Key performance indicator or 'measure'"""

    # perspective
    FINANCIAL = '1'
    CUSTOMER = '2'
    PROCESS = '3'
    LEARNING = '4'
    # direction
    UP = '1'
    DOWN = '2'
    # units
    VALUE = '1'
    RATIO = '2'
    PERCENT = '3'
    SECONDS = '4'
    MINUTES = '5'
    HOURS = '6'
    DAYS = '7'
    WEEKS = '8'
    MONTHS = '9'
    SCORE = '10'
    RATING = '11'
    NUMBER = '12'
    # calculations
    SUM = '1'
    AVG = '2'
    # reporting period
    MONTHLY = '1'
    QUARTERLY = '2'
    SEMI_ANNUALLY = '3'
    ANNUALLY = '4'

    PERSPECTIVE_CHOICES = (
        (FINANCIAL, _('Financial')),
        (CUSTOMER, _('Customer')),
        (PROCESS, _('Internal Process')),
        (LEARNING, _('Learning & Growth')),
    )

    DIRECTION_CHOICES = (
        (UP, _('Up')),
        (DOWN, _('Down')),
    )

    UNIT_CHOICES = (
        (VALUE, _('Value')),
        (NUMBER, _('Number')),
        (PERCENT, _('Percentage')),
        (RATIO, _('Ratio')),
        (SCORE, _('Score')),
        (RATING, _('Rating')),
        (SECONDS, _('Second(s)')),
        (MINUTES, _('Minute(s)')),
        (HOURS, _('Hour(s)')),
        (DAYS, _('Day(s)')),
        (WEEKS, _('Week(s)')),
        (MONTHS, _('Month(s)')),
    )

    CALCULATION_CHOICES = (
        (SUM, _('Sum')),
        (AVG, _('Average')),
    )

    REPORTING_PERIOD_CHOICES = (
        (MONTHLY, _('Monthly')),
        (QUARTERLY, _('Quarterly')),
        (SEMI_ANNUALLY, _('Semi-Annually')),
        (ANNUALLY, _('Annually')),
    )

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    perspective = models.CharField(_("Perspective"), max_length=1, choices=PERSPECTIVE_CHOICES, blank=False)
    target = models.DecimalField(_("Target"), max_digits=64, decimal_places=2, default=0)
    unit = models.CharField(_("Unit"), max_length=2, choices=UNIT_CHOICES, blank=False, default=VALUE)
    direction = models.CharField(_("Direction"), max_length=1, choices=DIRECTION_CHOICES, blank=False, default=UP)
    weight = models.DecimalField(_("Weight"), max_digits=5, decimal_places=2)
    reporting_period = models.CharField(_("Reporting Period"), max_length=1, choices=REPORTING_PERIOD_CHOICES, blank=False, default=ANNUALLY)
    calculation = models.CharField(_("Calculation"), max_length=1, choices=CALCULATION_CHOICES, blank=False, default=SUM)

    class Meta:
        verbose_name = _("KPI")
        verbose_name_plural = _("KPIs")
        ordering = ['name', '-weight']

    def __str__(self):
        return self.name

