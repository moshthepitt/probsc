from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.urls import reverse

import django_tables2 as tables

from .models import Scorecard, ScorecardKPI, Initiative, Score


class UserScorecardKPITable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    measure = tables.Column(verbose_name=_("Measure"), accessor='kpi', orderable=True)
    perspective = tables.Column(verbose_name=_("Perspective"), accessor='kpi', orderable=True)
    target = tables.Column(verbose_name=_("Target"), accessor='kpi', orderable=True)
    weight = tables.Column(verbose_name=_("Weight"), accessor='kpi', orderable=True)

    class Meta:
        model = ScorecardKPI
        exclude = ['created', 'modified', 'id', 'scorecard', 'score']
        sequence = ('kpi', 'measure', 'perspective', '...', 'action')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_kpi(self, record):
        return record.kpi.name

    def render_measure(self, record):
        return record.kpi.measure

    def render_target(self, record):
        return record.kpi.target

    def render_weight(self, record):
        return record.kpi.weight

    def render_perspective(self, record):
        return record.kpi.get_perspective_display()

    def render_action(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-default btn-xs list-initiative-button" data-pk="{pk}" data-toggle="tooltip" data-placement="left" title="{c}" aria-label="{c}">
              <span class="glyphicon glyphicon-th-list" aria-hidden="true"></span>
            </button>
            <button type="button" class="btn btn-default btn-xs add-initiative-button" data-pk="{pk}" data-toggle="tooltip" data-placement="left" title="{a}" aria-label="{a}">
              <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
            </button>
            <button type="button" class="btn btn-default btn-xs add-score-button" data-pk="{pk}" data-toggle="tooltip" data-placement="top" title="{b}" aria-label="{b}">
              <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
            </button>
            """,
            a=_("Add Initiative"),
            b=_("Report Scores"),
            c=_("View Initiatives"),
            pk=record.id
        )


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

    def render_name(self, record):
        return format_html(
            "<a href='{}'>{}</a>",
            reverse('scorecards:user_scorecard', args=[record.pk]),
            record.name
        )

    def render_action(self, record):
        return ""


class StaffScorecardTable(tables.Table):
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

    def render_name(self, record):
        return format_html(
            "<a href='#'>{}</a>",
            record.name
        )

    def render_action(self, record):
        return ""


class InitiativeTable(tables.Table):

    class Meta:
        model = Initiative
        exclude = ['created', 'modified', 'scorecard', 'kpi', 'id']
        sequence = ('date', 'name', 'description', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"


class ScoreTable(tables.Table):

    class Meta:
        model = Score
        exclude = ['created', 'modified', 'scorecard', 'kpi', 'id']
        sequence = ('date', 'value', 'notes', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
