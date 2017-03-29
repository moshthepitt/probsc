from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django_extensions.db.models import TimeStampedModel

from .managers import ScorecardManager

User = settings.AUTH_USER_MODEL


class Scorecard(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.PROTECT, blank=True, null=True)
    customer = models.ForeignKey('customers.Customer', verbose_name=_("Customer"), on_delete=models.PROTECT)
    kpis = models.ManyToManyField('kpis.KPI', verbose_name=_("KPIs"), blank=True)
    active = models.BooleanField(_("Active"), default=True)

    objects = ScorecardManager()

    class Meta:
        verbose_name = _("Scorecard")
        verbose_name_plural = _("Scorecards")

    def __str__(self):
        return self.name
