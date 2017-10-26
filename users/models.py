from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.urls import reverse

from django_extensions.db.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from .managers import UserProfileManager, DepartmentManager, PositionManager

User = settings.AUTH_USER_MODEL


class Department(MPTTModel, TimeStampedModel):

    """
    Departments in an organisation
    """
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    parent = TreeForeignKey('self', verbose_name=_("Parent"), null=True,
                            blank=True, related_name='children', db_index=True,
                            on_delete=models.PROTECT,
                            help_text=_("The parent department"))
    customer = models.ForeignKey(
        'customers.Customer', verbose_name=_("Customer"),
        on_delete=models.PROTECT)
    manager = models.ForeignKey(
        User, verbose_name=_("Manager"), on_delete=models.PROTECT,
        blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True)

    objects = DepartmentManager()

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ['name']

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return reverse('users:departments_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('users:departments_delete', args=[self.pk])

    def get_list_url(self):
        return reverse('users:departments_list')

    def __str__(self):
        return self.name


class Position(MPTTModel, TimeStampedModel):

    """
    Job positions in an organisation
    """
    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, default="")
    department = models.ForeignKey(
        Department, verbose_name=_("Department"), on_delete=models.PROTECT)
    parent = TreeForeignKey('self', verbose_name=_("Reports To"), null=True,
                            blank=True, related_name='children', db_index=True,
                            on_delete=models.PROTECT,
                            help_text=_("The parent Job Position"))
    supervisor = models.ForeignKey(
        User, verbose_name=_("Supervisor"), on_delete=models.PROTECT,
        blank=True, null=True)
    customer = models.ForeignKey(
        'customers.Customer', verbose_name=_("Customer"),
        on_delete=models.PROTECT)
    active = models.BooleanField(_("Active"), default=True)

    objects = PositionManager()

    class Meta:
        verbose_name = _("Job Positions")
        verbose_name_plural = _("Job Positions")
        ordering = ['name']

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return reverse('users:positions_edit', args=[self.pk])

    def get_delete_url(self):
        return reverse('users:positions_delete', args=[self.pk])

    def get_list_url(self):
        return reverse('users:positions_list')

    def __str__(self):
        return "{} - {}".format(self.department.name, self.name)


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
    position = models.ForeignKey(Position, verbose_name=_(
        "job Position"), on_delete=models.SET_NULL, blank=True, null=True,
        default=None)
    customer = models.ForeignKey('customers.Customer', verbose_name=_(
        "Customer"), on_delete=models.SET_NULL, blank=True, null=True,
        default=None)
    role = models.CharField(
        _("Role"), max_length=1, choices=MEMBER_ROLE_CHOICES, blank=False,
        default=MEMBER)
    active = models.BooleanField(
        _("Active"), default=True, help_text="Is the staff member actively "
                                             "employed?")

    objects = UserProfileManager()

    class Meta:
        verbose_name = _("Staff Member")
        verbose_name_plural = _("Staff Members")
        ordering = ['user__first_name', 'user__last_name', 'user__email']

    def get_name(self):
        if self.user.get_full_name():
            return self.user.get_full_name()
        if self.user.email:
            return self.user.email
        return self.user.username

    def get_initials(self):
        if self.user.first_name and self.user.last_name:
            return "{}{}".format(self.user.first_name[0],
                                 self.user.last_name[0])
        if self.user.first_name:
            return self.user.first_name[0]
        if self.user.last_name:
            return self.user.last_name[0]
        return self.user.email[0]

    def is_admin(self):
        return self.role == self.ADMIN

    def is_editor(self):
        return self.role == self.EDITOR

    def can_edit(self):
        return self.role == self.EDITOR or self.role == self.ADMIN

    def get_subordinates(self):
        """
        Returns a queryset of UserProfile objects which report to this
        userprofile
        """
        if self.position:
            queryset = UserProfile.objects.active().exclude(
                id=self.id).filter(
                models.Q(
                    position__supervisor=self.user) | models.Q(
                    position__department__manager=self.user) | models.Q(
                    position__parent=self.position))
        else:
            queryset = UserProfile.objects.active().exclude(
                id=self.id).filter(
                models.Q(
                    position__supervisor=self.user) | models.Q(
                    position__department__manager=self.user))
        return queryset

    def has_subordinates(self):
        return self.get_subordinates().exists()

    def get_absolute_url(self):
        return "#"

    def get_edit_url(self):
        return reverse('users:userprofiles_edit', args=[self.pk])

    def get_delete_url(self):
        return "#"

    def get_list_url(self):
        return reverse('users:userprofiles_list')

    def __str__(self):
        return _("{user}").format(user=self.get_name())
