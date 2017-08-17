from decimal import Decimal, DecimalException
import statistics

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel

from core.utils import PathAndRename
from .managers import ScorecardManager, ScorecardKPIManager, ScoreKPIManager
from .utils import bsc_rating, get_contextual_rating, get_inverse_contextual_rating

User = settings.AUTH_USER_MODEL


class Scorecard(TimeStampedModel):

    """
    Each staff member can have one ore more scorecards
    A scorecard is a group of performance indicators that relate to:
        1. a staff member
        2. an appraissal period
    """
    name = models.TextField(_("Name"), max_length=255)
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

    def get_report(self, this_round=1):
        total, financial, customer = Decimal(0.00), Decimal(0.00), Decimal(0.00)
        process, learning = Decimal(0.00), Decimal(0.00)
        scorecard_kpis = ScorecardKPI.objects.filter(scorecard=self)
        for scorecard_kpi in scorecard_kpis:
            scorecard_kpi.score = scorecard_kpi.get_score(this_round=this_round)
            if scorecard_kpi.kpi.perspective == scorecard_kpi.kpi.FINANCIAL:
                financial = financial + Decimal(scorecard_kpi.score)
            if scorecard_kpi.kpi.perspective == scorecard_kpi.kpi.CUSTOMER:
                customer = customer + Decimal(scorecard_kpi.score)
            if scorecard_kpi.kpi.perspective == scorecard_kpi.kpi.PROCESS:
                process = process + Decimal(scorecard_kpi.score)
            if scorecard_kpi.kpi.perspective == scorecard_kpi.kpi.LEARNING:
                learning = learning + Decimal(scorecard_kpi.score)
            total = total + Decimal(scorecard_kpi.score)
        if self.customer.best == self.customer.FIVE:
            contextual_rating = get_contextual_rating(total)
        else:
            contextual_rating = get_inverse_contextual_rating(total)
        return {'kpis': scorecard_kpis, 'total': total, 'financial': financial,
                'customer': customer, 'process': process, 'learning': learning,
                'contextual_rating': contextual_rating}

    class Meta:
        verbose_name = _("Scorecard")
        verbose_name_plural = _("Scorecards")
        ordering = ['-year', 'name']

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return reverse('scorecards:scorecards_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('scorecards:scorecards_delete', args=[self.pk])

    def get_list_url(self):
        return reverse('scorecards:scorecards_list')

    def get_kpis_list_url(self):
        return reverse('scorecards:scorecards_kpis_list', args=[self.pk])

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

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return "#"

    def get_delete_url(self):
        return "#"

    def get_list_url(self):
        return "#"

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

    objects = ScoreKPIManager()

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
    scorecard = models.ForeignKey(Scorecard, verbose_name=_("Scorecard"), on_delete=models.CASCADE)
    kpi = models.ForeignKey('kpis.KPI', verbose_name=_("KPI"), on_delete=models.CASCADE)
    score = models.DecimalField(
        _("Score"), max_digits=64, decimal_places=2, default=0, help_text=_("The KPI BSC score"))

    objects = ScorecardKPIManager()

    def get_actual(self, this_round=1):
        """
        Get the score as a percentage of the target
        """
        records_no = self.kpi.get_number_of_scores()
        records = Score.objects.filter(
            scorecard=self.scorecard, kpi=self.kpi, review_round=this_round)[:records_no]
        # return 0 if no records
        if not records:
            return Decimal(0)
        values_list = [x.value for x in records]
        # get the value
        if self.kpi.calculation == self.kpi.AVG:
            value = statistics.mean(values_list)
        else:
            value = sum(values_list)
        # calculate actual as a percentage of target
        value = Decimal(value)
        if value == self.kpi.target:
            actual = 1 * Decimal(100)
        elif self.kpi.direction == self.kpi.DOWN:
            if value == Decimal(0):
                # dirty hack to avoid division by zero
                actual = (self.kpi.target / Decimal(0.0000000001)) * Decimal(100)
            else:
                actual = (self.kpi.target / value) * Decimal(100)
        else:
            # direction is UP
            if self.kpi.target == Decimal(0):
                # dirty hack to avoid division by zero
                actual = (value / Decimal(0.0000000001)) * Decimal(100)
            else:
                actual = (value / self.kpi.target) * Decimal(100)
        return actual

    def get_actual_rating(self, this_round=1):
        actual = self.get_actual(this_round)
        return bsc_rating(actual, customer=self.scorecard.customer)

    def get_score(self, this_round=1, do_save=False):

        # get the score == weighted rating
        if not do_save:
            return self.score
        # else calculate and save it
        score = Decimal(0.00)
        if Score.objects.filter(scorecard=self.scorecard, kpi=self.kpi, review_round=this_round).exists():
            actual_rating = self.get_actual_rating(this_round)
            try:
                weight_percentage = self.kpi.weight / Decimal(100)
            except DecimalException:
                score = Decimal(0)
            else:
                score = weight_percentage * actual_rating
        self.score = score
        self.save()
        return score

    def get_actual_rating_from_score(self):
        try:
            weight_percentage = self.kpi.weight / Decimal(100)
        except DecimalException:
            actual = Decimal(0)
        else:
            actual = self.get_score() / weight_percentage
        if actual > Decimal(5.0):
            return Decimal(5.0)
        return actual

    def contextual_rating(self):
        if self.scorecard.customer.best == self.scorecard.customer.FIVE:
            return get_contextual_rating(self.get_actual_rating_from_score())
        else:
            return get_inverse_contextual_rating(self.get_actual_rating_from_score())

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

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return "#"

    def get_delete_url(self):
        return "#"

    def get_list_url(self):
        return "#"

    def __str__(self):
        return self.name
