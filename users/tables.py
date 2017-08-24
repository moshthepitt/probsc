from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.urls import reverse

import django_tables2 as tables

from .models import Department, Position, UserProfile


class DepartmentTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Department
        exclude = ['created', 'modified', 'description', 'id',
                   'customer', 'lft', 'rght', 'tree_id', 'level']
        sequence = ('name', 'parent', 'manager', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            record.get_edit_url(),
            record.get_delete_url()
        )

    def render_manager(self, record):
        return record.manager.userprofile.get_name()


class PositionTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Position
        exclude = ['created', 'modified', 'description', 'id',
                   'customer', 'lft', 'rght', 'tree_id', 'level']
        sequence = ('name',
                    'department',
                    'parent',
                    'supervisor',
                    'active',
                    '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>',
            record.get_edit_url(),
            record.get_delete_url()
        )

    def render_supervisor(self, record):
        return record.supervisor.userprofile.get_name()


class UserProfileTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    email = tables.EmailColumn(verbose_name=_("Email"),
                               accessor='user.email',
                               orderable=True)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = UserProfile
        exclude = ['customer', 'created_on', 'updated_on', 'id']
        sequence = ('user', 'email', 'position', 'role', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html(
            '<a href="{}">Edit</a>', record.get_edit_url()
        )

    def render_user(self, record):
        return record.get_name()

    def render_email(self, record):
        return record.user.email


class SubordinatesTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    email = tables.EmailColumn(verbose_name=_("Email"),
                               accessor='user.email',
                               orderable=True)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = UserProfile
        exclude = ['customer', 'created_on', 'updated_on', 'id', 'role']
        sequence = ('user', 'email', 'position', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html(
            "<a href='{}'>Scorecards</a>",
            reverse('scorecards:staff_scorecards', args=[record.user.pk])
        )

    def render_user(self, record):
        return record.get_name()

    def render_email(self, record):
        return record.user.email
