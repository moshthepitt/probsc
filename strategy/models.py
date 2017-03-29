from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from .managers import ObjectiveManager, StrategicThemeManager


class StrategicTheme(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    customer = models.ForeignKey('customers.Customer', verbose_name=_("Customer"), on_delete=models.PROTECT)
    active = models.BooleanField(_("Active"), default=True)

    objects = StrategicThemeManager()

    class Meta:
        verbose_name = _("Strategic Theme")
        verbose_name_plural = _("Strategic Themes")
        ordering = ['name']

    def __str__(self):
        return self.name


class Objective(MPTTModel, TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    strategic_theme = models.ForeignKey(StrategicTheme, verbose_name=_("Strategic Theme"), on_delete=models.PROTECT)
    parent = TreeForeignKey('self', verbose_name=_("Contributes to"), null=True, blank=True, related_name='children', db_index=True)
    customer = models.ForeignKey('customers.Customer', verbose_name=_("Customer"), on_delete=models.PROTECT)
    active = models.BooleanField(_("Active"), default=True)

    objects = ObjectiveManager()

    class Meta:
        verbose_name = _("Objective")
        verbose_name_plural = _("Objectives")
        ordering = ['name', 'strategic_theme']

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

