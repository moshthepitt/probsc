from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomerManager


class Customer(TimeStampedModel):
    """
    Represents a person/organisation that uses ProBSC
    """
    name = models.CharField(_("Name"), max_length=255)
    email = models.EmailField(_('Email Address'), blank=True)
    phone = PhoneNumberField(_('Phone Number'), max_length=255, blank=True)
    description = models.TextField(_("Description"), blank=True, default="")
    active = models.BooleanField(_("Active"), default=True)

    objecs = CustomerManager()

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        ordering = ['name']

    def __str__(self):
        return self.name
