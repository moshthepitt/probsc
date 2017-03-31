from decimal import Decimal
import statistics

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from django_extensions.db.models import TimeStampedModel

from core.utils import PathAndRename
from .managers import ScorecardManager
from .utils import bsc_rating

User = settings.AUTH_USER_MODEL


class Scorecard(TimeStampedModel):

    """
    Each staff member can have one ore more scorecards
    A scorecard is a group of performance indicators that relate to:
        1. a staff member
        2. an appraissal period
    """
    name = models.CharField(_("Name"), max_length=255)
    year = models.PositiveIntegerField(
        _("Year"), default=timezone.now().year, validators=[MinValueValidator(2012), MaxValueValidator(3000)])
    description = models.TextField(_("Description"), blank=True, default="")
    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey(
        'customers.Customer', verbose_name=_("Customer"), on_delete=models.PROTECT)
    kpis = models.ManyToManyField(
        'kpis.KPI', through='ScorecardKPI', verbose_name=_("KPIs"), blank=True)
    active = models.BooleanField(_("Active"), default=True)

    objects = ScorecardManager()

    class Meta:
        verbose_name = _("Scorecard")
        verbose_name_plural = _("Scorecards")
        ordering = ['year', 'name']

    def __str__(self):
        return self.name


class Evidence(TimeStampedModel):

    """
    Scorecard evidence that is an uploaded file
    """
    scorecard = models.ForeignKey(Scorecard, verbose_name=_("Scorecard"), on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=255)
    date = models.DateField(_("Date"), default=timezone.now)
    file = models.FileField(_("File"), upload_to=PathAndRename(
        "files/evidence/{}/".format(timezone.now().year)), max_length=255)

    class Meta:
        verbose_name = _("Evidence")
        verbose_name_plural = _("Evidences")
        ordering = ['name']

    def __str__(self):
        return self.name


class Score(TimeStampedModel):

    """
    Records the performance score of KPIs for a Scorecard on a partcular date
    """
    date = models.DateField(_("Date"), default=timezone.now)
    scorecard = models.ForeignKey(Scorecard, verbose_name=_("Scorecard"), on_delete=models.PROTECT)
    kpi = models.ForeignKey('kpis.KPI', verbose_name=_("KPI"), on_delete=models.PROTECT)
    value = models.DecimalField(_("Value"), max_digits=64, decimal_places=2, default=0)
    review_round = models.PositiveIntegerField(
        _("Review Round"), default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(_("Notes"), blank=True, default="")

    def get_score(self):
        if self.kpi.direction == self.kpi.UP:
            return ((self.value - self.kpi.baseline) / (self.kpi.target - self.kpi.baseline)) * Decimal(0)
        elif self.kpi.direction == self.kpi.DOWN:
            return ((self.kpi.baseline - self.value) / (self.kpi.baseline - self.kpi.target)) * Decimal(0)

    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")
        ordering = ['-date']

    def __str__(self):
        return "{} {} {}".format(self.date, self.scorecard, self.kpi)


class ScorecardKPI(TimeStampedModel):

    """
    A way to group KPIs in a scorecard and have additional information
    that relates to the KPI in the scorecard
    """
    scorecard = models.ForeignKey(Scorecard, verbose_name=_("Scorecard"), on_delete=models.PROTECT)
    kpi = models.ForeignKey('kpis.KPI', verbose_name=_("KPI"), on_delete=models.PROTECT)
    score = models.DecimalField(
        _("Score"), max_digits=64, decimal_places=2, default=0, help_text=_("The KPI BSC score"))

    def get_score(self, this_round=1, do_save=True):
        records_no = self.kpi.get_number_of_scores()
        records = Score.objects.filter(
            scorecard=self.scorecard, kpi=self.kpi, review_round=this_round)[:records_no]
        values_list = [x.value for x in records]
        # get the value
        if self.kpi.calculation == self.kpi.AVG:
            value = statistics.mean(values_list)
        else:
            value = sum(values_list)
        # calculate actual as a % of target
        value = Decimal(value)
        if self.kpi.direction == self.kpi.UP:
            actual = ((value - self.kpi.baseline) /
                      (self.kpi.target - self.kpi.baseline)) * Decimal(100)
        elif self.kpi.direction == self.kpi.DOWN:
            actual = ((self.kpi.baseline - value) /
                      (self.kpi.baseline - self.kpi.target)) * Decimal(100)
        # get the score
        score = (self.kpi.weight / Decimal(100)) * bsc_rating(actual)
        if do_save:
            self.score = score
            self.save()
        return score

    class Meta:
        verbose_name = _("Scorecard KPI")
        verbose_name_plural = _("Scorecard KPIs")
        ordering = ['scorecard', 'kpi']

    def __str__(self):
        return "{} {}".format(self.scorecard, self.kpi)


class Initiative(TimeStampedModel):

    """
    Represent specific activities undertaken in the achievment of KPIs
    """
    date = models.DateField(_("Date"), default=timezone.now)
    scorecard = models.ForeignKey(Scorecard, verbose_name=_("Scorecard"), on_delete=models.PROTECT)
    kpi = models.ForeignKey('kpis.KPI', verbose_name=_("KPI"), on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")

    class Meta:
        verbose_name = _("Initiative")
        verbose_name_plural = _("Initiatives")
        ordering = ['-date']

    def __str__(self):
        return self.name
