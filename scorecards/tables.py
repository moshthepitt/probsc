from django.utils.html import format_html
from django.utils.translation import ugettext as _

import django_tables2 as tables

from .models import Scorecard


class ScorecardTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Scorecard
        exclude = ['created', 'modified', 'description', 'id', 'customer', 'kpis']
        sequence = ('name', 'user', 'year', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_user(self, record):
        return record.user.userprofile.get_name()

    def render_action(self, record):
        return format_html(
            '<a href="{}">Manage KPIs</a> | <a href="{}">Edit</a> | <a href="{}">Delete</a>',
            record.get_kpis_list_url(),
            record.get_edit_url(),
            record.get_delete_url()
        )


class UserScorecardTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Scorecard
        exclude = ['created', 'modified', 'description', 'id', 'customer', 'kpis', 'user']
        sequence = ('name', 'year', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_name(self, record):
        return format_html(
            "<a href='#'>{}</a>",
            record.name
        )

    def render_action(self, record):
        return ""
