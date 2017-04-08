from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

User = settings.AUTH_USER_MODEL


@python_2_unicode_compatible
class UserProfile(models.Model):
    """
    Model used to store more information on users
    """

    ADMIN = '1'
    MEMBER = '2'
    EDITOR = '3'

    MEMBER_ROLE_CHOICES = (
        (ADMIN, _('Admin')),
        (EDITOR, _('Editor')),
        (MEMBER, _('Member')),
    )

    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated on"), auto_now=True)
    user = models.OneToOneField(User, verbose_name=_("User"))
    customer = models.ForeignKey('customers.Customer', verbose_name=_("Customer"), on_delete=models.SET_NULL, blank=True, null=True, default=None)
    role = models.CharField(_("Role"), max_length=1, choices=MEMBER_ROLE_CHOICES, blank=False, default=MEMBER)
    active = models.BooleanField(_("Active"), default=True, help_text="Is the staff member still actively employed?")

    def get_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.email

    def get_initials(self):
        if self.user.first_name and self.user.last_name:
            return "{}{}".format(self.user.first_name[0], self.user.last_name[0])
        if self.user.first_name:
            return self.user.first_name[0]
        if self.user.last_name:
            return self.user.last_name[0]
        return self.user.email[0]

    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return _("{user}'s profile").format(user=self.user)
