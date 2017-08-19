from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel

from .managers import KPIManager


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
    BI_MONTHLY = '2'
    QUARTERLY = '3'
    SEMI_ANNUALLY = '4'
    ANNUALLY = '5'
    # reporting method
    MANUAL = '1'
    AUTOMATED = '2'

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
        (BI_MONTHLY, _('Bi-Monthly')),
        (QUARTERLY, _('Quarterly')),
        (SEMI_ANNUALLY, _('Semi-Annually')),
        (ANNUALLY, _('Annually')),
    )

    REPORTING_METHOD_CHOICES = (
        (MANUAL, _('Manual')),
        (AUTOMATED, _('Automated')),
    )

    # constants
    NO_MONTHLY = 12
    NO_BI_MONTHLY = 6
    NO_QUARTERLY = 4
    NO_SEMI_ANNUALLY = 2
    NO_ANNUALLY = 1

    objective = models.ForeignKey(
        'strategy.Objective', verbose_name=_("Objective"), on_delete=models.PROTECT)
    name = models.TextField(_("Key Performance Indicator"), max_length=255)
    measure = models.TextField(_("Measure"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    perspective = models.CharField(
        _("Perspective"), max_length=1, choices=PERSPECTIVE_CHOICES, blank=False)
    baseline = models.DecimalField(_("Base Line"), max_digits=64, decimal_places=2, default=0)
    target = models.DecimalField(_("Target"), max_digits=64, decimal_places=2, default=0)
    unit = models.CharField(
        _("Unit"), max_length=2, choices=UNIT_CHOICES, blank=False, default=VALUE)
    direction = models.CharField(
        _("Direction"), max_length=1, choices=DIRECTION_CHOICES, blank=False, default=UP)
    weight = models.DecimalField(_("Weight"), max_digits=5, decimal_places=2)
    reporting_period = models.CharField(
        _("Reporting Period"), max_length=1, choices=REPORTING_PERIOD_CHOICES, blank=False, default=ANNUALLY)
    calculation = models.CharField(
        _("Calculation"), max_length=1, choices=CALCULATION_CHOICES, blank=False, default=SUM)
    reporting_method = models.CharField(
        _("Reporting Method"), max_length=1, choices=REPORTING_METHOD_CHOICES, blank=False, default=MANUAL)
    customer = models.ForeignKey(
        'customers.Customer', verbose_name=_("Customer"), on_delete=models.PROTECT)
    active = models.BooleanField(_("Active"), default=True)

    objects = KPIManager()

    class Meta:
        verbose_name = _("KPI")
        verbose_name_plural = _("KPIs")
        ordering = ['perspective', 'name', '-weight']

    def __str__(self):
        return self.name

    def get_number_of_scores(self):
        if self.reporting_period == self.ANNUALLY:
            return self.NO_ANNUALLY
        if self.reporting_period == self.SEMI_ANNUALLY:
            return self.NO_SEMI_ANNUALLY
        if self.reporting_period == self.QUARTERLY:
            return self.NO_QUARTERLY
        if self.reporting_period == self.BI_MONTHLY:
            return self.NO_BI_MONTHLY
        if self.reporting_period == self.MONTHLY:
            return self.NO_MONTHLY
        return self.NO_ANNUALLY

    def get_target_per_score(self):
        """
        If the target is to be met, this should be the minimum value of each
        score
        """
        pass

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return reverse('kpis:kpis_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('kpis:kpis_delete', args=[self.pk])

    def get_list_url(self):
        return reverse('kpis:kpis_list')
