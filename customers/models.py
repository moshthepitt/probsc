from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomerManager


class Customer(TimeStampedModel):

    """
    Represents a person/organization that uses ProBSC
    """

    ONE = 1
    FIVE = 5

    BEST_RATING_CHOICES = (
        (ONE, _('1')),
        (FIVE, _('5')),
    )

    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_('Email Address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    description = models.TextField(_("Description"), blank=True, default="")
    financial_year_end_day = models.PositiveSmallIntegerField(
        _("Financial Year End Day"), default=31, validators=[MinValueValidator(1), MaxValueValidator(31)])
    financial_year_end_month = models.PositiveSmallIntegerField(
        _("Financial Year End Month"), default=12, validators=[MinValueValidator(1), MaxValueValidator(12)])
    review_rounds = models.PositiveSmallIntegerField(
        _("Rounds of Review"),
        default=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)],
        help_text=_("How many times is each scorecard reviewed? e.g. "
                    "self review, supervisor review, etc"))
    best = models.IntegerField(
        _("Best Rating"),
        help_text=_("Which value represents the best rating"),
        max_length=1,
        choices=BEST_RATING_CHOICES,
        blank=False,
        default=FIVE)
    active = models.BooleanField(_("Active"), default=True)

    objects = CustomerManager()

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_bsc_rating_dict(self):
        if self.best == self.FIVE:
            return settings.BSC_RATING
        return settings.BSC_INVERSE_RATING
