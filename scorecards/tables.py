from decimal import Decimal

from django.utils.html import format_html
from django.utils.translation import ugettext as _
from django.urls import reverse

import django_tables2 as tables

from .models import Scorecard, ScorecardKPI, Initiative, Score, Evidence

TWOPLACES = Decimal(10) ** -2


class ScorecardReportKPITable(tables.Table):
    measure = tables.Column(verbose_name=_("Measure"),
                            accessor='kpi',
                            orderable=True)
    perspective = tables.Column(verbose_name=_("Perspective"),
                                accessor='kpi',
                                orderable=True)
    target = tables.Column(verbose_name=_("Target"),
                           accessor='kpi',
                           orderable=True)
    weight = tables.Column(verbose_name=_("Weight"),
                           accessor='kpi',
                           orderable=True)
    direction = tables.Column(verbose_name=_("Direction"),
                              accessor='kpi',
                              orderable=True)
    reporting_period = tables.Column(
        verbose_name=_("Reporting Period"), accessor='kpi', orderable=True)
    initiatives = tables.Column(verbose_name=_("Initiatives"),
                                accessor='pk',
                                orderable=False)
    rating = tables.Column(verbose_name=_("Rating"),
                           accessor='pk',
                           orderable=True)
    scores = tables.Column(verbose_name=_("Scores"),
                           accessor='pk',
                           orderable=False,
                           attrs={'th': {'width': '7%'}})

    class Meta:
        model = ScorecardKPI
        exclude = ['created', 'modified', 'id', 'scorecard', 'score']
        sequence = ('kpi', 'measure', 'perspective', 'target', 'direction',
                    'reporting_period', '...', 'weight', 'rating',
                    'initiatives', 'scores')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_kpi(self, record):
        return record.kpi.name

    def render_measure(self, record):
        return record.kpi.measure

    def render_target(self, record):
        return record.kpi.target

    def render_weight(self, record):
        return "{}%".format(record.kpi.weight)

    def render_direction(self, record):
        return record.kpi.get_direction_display()

    def render_reporting_period(self, record):
        return record.kpi.get_reporting_period_display()

    def render_perspective(self, record):
        return record.kpi.get_perspective_display()

    def render_rating(self, record):
        return record.get_actual_rating_from_score().quantize(TWOPLACES)

    def render_initiatives(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-{contextual_rating} btn-xs
                list-initiative-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="left" title="{c}" aria-label="{c}">
              <span class="glyphicon glyphicon-th-list" aria-hidden="true">
              </span>
            </button>
            """,
            c=_("View Initiatives"),
            pk=record.id,
            contextual_rating=record.contextual_rating()
        )

    def render_scores(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-{contextual_rating} btn-xs
                list-score-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="left" title="{c}" aria-label="{c}">
              <span class="glyphicon glyphicon-ok" aria-hidden="true"></span>
            </button>
            <button type="button" class="btn btn-{contextual_rating} btn-xs
                score-graph-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="left" title="{d}" aria-label="{d}">
              <span class="glyphicon glyphicon-signal" aria-hidden="true">
              </span>
            </button>
            """,
            c=_("View Scores"),
            d=_("View Graphs"),
            pk=record.id,
            contextual_rating=record.contextual_rating()
        )


class UserScorecardKPITable(tables.Table):
    measure = tables.Column(verbose_name=_("Measure"),
                            accessor='kpi',
                            orderable=True)
    perspective = tables.Column(verbose_name=_("Perspective"),
                                accessor='kpi',
                                orderable=True)
    target = tables.Column(verbose_name=_("Target"),
                           accessor='kpi',
                           orderable=True)
    weight = tables.Column(verbose_name=_("Weight"),
                           accessor='kpi',
                           orderable=True)
    direction = tables.Column(verbose_name=_("Direction"),
                              accessor='kpi',
                              orderable=True)
    reporting_period = tables.Column(verbose_name=_("Reporting Period"),
                                     accessor='kpi',
                                     orderable=True)
    initiatives = tables.Column(verbose_name=_("Initiatives"),
                                accessor='pk',
                                orderable=False,
                                attrs={'th': {'width': '7%'}})
    action = tables.Column(verbose_name=_("Scores"),
                           accessor='pk',
                           orderable=False,
                           attrs={'th': {'width': '7%'}})

    class Meta:
        model = ScorecardKPI
        exclude = ['created', 'modified', 'id', 'scorecard', 'score']
        sequence = ('kpi', 'measure', 'perspective', 'target', 'direction',
                    'reporting_period', '...', 'weight', 'initiatives',
                    'action')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_kpi(self, record):
        return record.kpi.name

    def render_measure(self, record):
        return record.kpi.measure

    def render_target(self, record):
        return record.kpi.target

    def render_weight(self, record):
        return "{}%".format(record.kpi.weight)

    def render_direction(self, record):
        return record.kpi.get_direction_display()

    def render_reporting_period(self, record):
        return record.kpi.get_reporting_period_display()

    def render_perspective(self, record):
        return record.kpi.get_perspective_display()

    def render_initiatives(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-{contextual_rating} btn-xs
                list-initiative-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="left" title="{c}" aria-label="{c}">
              <span class="glyphicon glyphicon-th-list" aria-hidden="true">
              </span>
            </button>
            <button type="button" class="btn btn-{contextual_rating} btn-xs
                add-initiative-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="left" title="{a}" aria-label="{a}">
              <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
            </button>
            """,
            a=_("Add Initiative"),
            c=_("View Initiatives"),
            pk=record.id,
            contextual_rating=record.contextual_rating()
        )

    def render_action(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-{contextual_rating} btn-xs
                score-graph-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="left" title="{d}" aria-label="{d}">
              <span class="glyphicon glyphicon-signal" aria-hidden="true">
              </span>
            </button>
            <button type="button" class="btn btn-{contextual_rating}
                btn-xs add-score-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="top" title="{b}" aria-label="{b}">
              <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
            </button>
            """,
            b=_("Report Scores"),
            d=_("View Graphs"),
            pk=record.id,
            actual=record.get_actual_rating_from_score().quantize(TWOPLACES),
            contextual_rating=record.contextual_rating()
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
        exclude = ['created',
                   'modified',
                   'description',
                   'id',
                   'customer',
                   'kpis',
                   'approved_by',
                   'approval_note']
        sequence = ('name', 'user', 'year', 'approved', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_user(self, record):
        return record.user.userprofile.get_name()

    def render_action(self, record):
        return format_html(
            '<a href="{a}">Approve</a> | <a href="{b}">Manage KPIs</a> | '
            '<a href="{e}">Evidence</a> | <a href="{c}">Edit</a> '
            '| <a href="{d}">Delete</a>',
            a=record.get_approval_url(),
            b=record.get_kpis_list_url(),
            c=record.get_edit_url(),
            d=record.get_delete_url(),
            e=reverse('scorecards:scorecard_evidence_list', args=[record.id])
        )


class ScorecardReportTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False,
                           exclude_from_export=True)
    score = tables.Column(verbose_name=_("Score"),
                          accessor='pk',
                          orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Scorecard
        exclude = ['created',
                   'modified',
                   'description',
                   'id',
                   'customer',
                   'kpis',
                   'approved_by',
                   'approval_note']
        sequence = ('name',
                    'user',
                    'year',
                    'approved',
                    'active',
                    'score',
                    '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_user(self, record):
        return record.user.userprofile.get_name()

    def render_score(self, record):
        report = record.get_report()
        return format_html(
            '<span class="text text-{b}"><strong>{a}</strong></span>',
            a=report['total'].quantize(TWOPLACES),
            b=report['contextual_rating'],
        )

    def value_score(self, record):
        report = record.get_report()
        return report['total'].quantize(TWOPLACES)

    def render_action(self, record):
        return format_html(
            "<a href='{c}'>{d}</a>",
            c=reverse('scorecards:scorecard_report', args=[record.pk]),
            d=_("View Report")
        )


class UserScorecardTable(tables.Table):
    edit = tables.Column(verbose_name=_("Edit"),
                         accessor='pk',
                         orderable=False, exclude_from_export=True)
    action = tables.Column(verbose_name=_("Reporting"),
                           accessor='pk',
                           orderable=False, exclude_from_export=True)
    score = tables.Column(verbose_name=_("Score"),
                          accessor='pk',
                          orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Scorecard
        exclude = ['created',
                   'modified',
                   'description',
                   'id',
                   'customer',
                   'kpis',
                   'user',
                   'approval_note']
        sequence = ('name',
                    'year',
                    'approved',
                    'approved_by',
                    'active',
                    'score',
                    'edit',
                    '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_name(self, record):
        return format_html(
            "<a href='{}'>{}</a>",
            reverse('scorecards:user_scorecard', args=[record.pk]),
            record.name
        )

    def value_name(self, record):
        return record.name

    def render_approved_by(self, record):
        return record.approved_by.userprofile.get_name()

    def render_score(self, record):
        report = record.get_report()
        return format_html(
            '<span class="text text-{b}"><strong>{a}</strong></span>',
            a=report['total'].quantize(TWOPLACES),
            b=report['contextual_rating'],
        )

    def value_score(self, record):
        report = record.get_report()
        return report['total'].quantize(TWOPLACES)

    def render_action(self, record):
        return format_html(
            "<a href='{e}'>{f}</a> | <a href='{a}'>{b}</a> | <a href='{c}'>{d}"
            "</a>",
            a=reverse('scorecards:user_scorecard', args=[record.pk]),
            b=_("Record Scores"),
            c=reverse('scorecards:scorecard_report', args=[record.pk]),
            d=_("View Report"),
            e="{}?next={}".format(
                reverse('scorecards:scorecard_evidence_add',
                        args=[record.pk]),
                reverse('scorecards:user_scorecards')
                ),
            f=_("Add Evidence")
        )

    def render_edit(self, record):
        return format_html(
            '<a href="{a}">Manage KPIs</a> | <a href="{d}">Evidence</a> | '
            '<a href="{b}">Edit</a> | <a href="{c}">Delete</a>',
            a=reverse('scorecards:user_scorecards_kpis_list',
                      args=[record.id]),
            b=reverse('scorecards:user_scorecards_edit', args=[record.id]),
            c=reverse('scorecards:user_scorecards_delete', args=[record.id]),
            d=reverse('scorecards:scorecard_evidence_list', args=[record.id]),
        )


class StaffScorecardTable(tables.Table):
    action = tables.Column(verbose_name="",
                           accessor='pk',
                           orderable=False)
    score = tables.Column(verbose_name=_("Score"),
                          accessor='pk',
                          orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = Scorecard
        exclude = ['created',
                   'modified',
                   'description',
                   'id',
                   'customer',
                   'kpis',
                   'user',
                   'approval_note']
        sequence = ('name',
                    'year',
                    'approved',
                    'approved_by',
                    'active',
                    'score',
                    '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_name(self, record):
        return format_html(
            "<a href='#'>{}</a>",
            record.name
        )

    def render_approved_by(self, record):
        return record.approved_by.userprofile.get_name()

    def render_score(self, record):
        report = record.get_report()
        return format_html(
            '<span class="text text-{b}"><strong>{a}</strong></span>',
            a=report['total'].quantize(TWOPLACES),
            b=report['contextual_rating'],
        )

    def render_action(self, record):
        return format_html(
            "<a href='{a}'>{b}</a> | <a href='{e}'>{f}</a> | <a href='{c}'>{d}"
            "</a>",
            a=reverse('scorecards:staff_scorecards_approve', args=[record.pk]),
            b=_("Approve"),
            c=reverse('scorecards:scorecard_report', args=[record.pk]),
            d=_("View Report"),
            e=reverse('scorecards:scorecard_evidence_list', args=[record.id]),
            f=_("Evidence"),
        )


class InitiativeTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)

    class Meta:
        model = Initiative
        exclude = ['created', 'modified', 'scorecard', 'kpi', 'id']
        sequence = ('date', 'name', 'description', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_action(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-danger btn-xs
                delete-initiative-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="top" title="{b}" aria-label="{b}">
              <span class="glyphicon glyphicon-trash" aria-hidden="true">
              </span>
            </button>
            """,
            b=_("Delete"),
            pk=record.id
        )


class ScoreTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)

    class Meta:
        model = Score
        exclude = ['created',
                   'modified',
                   'scorecard',
                   'kpi',
                   'id',
                   'review_round']
        sequence = ('date', 'value', 'notes', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_action(self, record):
        return format_html(
            """
            <button type="button" class="btn btn-danger btn-xs
                delete-score-button" data-pk="{pk}" data-toggle="tooltip"
                data-placement="top" title="{b}" aria-label="{b}">
              <span class="glyphicon glyphicon-trash" aria-hidden="true">
              </span>
            </button>
            """,
            b=_("Delete"),
            pk=record.id
        )


class EvidenceTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)

    class Meta:
        model = Evidence
        exclude = ['created',
                   'modified',
                   'id']
        sequence = ('date', 'name', 'scorecard', 'file', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_action(self, record):
        return format_html(
            "<a href='{a}'>{b}</a> | <a href='{c}'>{d}</a>",
            a=reverse('scorecards:scorecard_evidence_edit',
                      args=[record.pk, record.scorecard.pk]),
            b=_("Edit"),
            c=reverse('scorecards:scorecard_evidence_delete',
                      args=[record.pk, record.scorecard.pk]),
            d=_("Delete")
        )
