from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from django_extensions.db.models import TimeStampedModel

from core.utils import PathAndRename
from .managers import ScorecardManager

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
    kpis = models.ManyToManyField('kpis.KPI', verbose_name=_("KPIs"), blank=True)
    active = models.BooleanField(_("Active"), default=True)

    objects = ScorecardManager()

    class Meta:
        verbose_name = _("Scorecard")
        verbose_name_plural = _("Scorecards")

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
    score = models.DecimalField(_("Score"), max_digits=64, decimal_places=2, default=0, help_text=_(
        "Performance achieved as a percentage of the target"))
    review_round = models.PositiveIntegerField(
        _("Review Round"), default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(_("Notes"), blank=True, default="")

    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")

    def __str__(self):
        return "{} {} {}".format(self.date, self.scorecard, self.kpi)


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

    def __str__(self):
        return self.name
