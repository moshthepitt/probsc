from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField


class Customer(TimeStampedModel):
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_('Email Address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    description = models.TextField(_("Description"), blank=True, default="")
    active = models.BooleanField(_("Active"), default=True)

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['name']

    def __str__(self):
        return self.name
