from django.utils.html import format_html
from django.utils.translation import ugettext as _

import django_tables2 as tables

from .models import KPI


class KPITable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = KPI
        exclude = ['created', 'modified', 'description', 'id', 'baseline',
                   'customer', 'reporting_method', 'objective', 'calculation']
        sequence = ('name', 'perspective', 'measure', 'target', 'unit',
                    'direction', 'weight', 'reporting_period', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>', record.get_edit_url(), record.get_delete_url()
        )


class ScorecardKPITable(KPITable):

    class Meta:
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"

    def render_action(self, record):
        return format_html(
            '<a href="{}">Edit</a> | <a href="{}">Delete</a>', "xx", "yy"
        )

    def __init__(self, *args, **kwargs):
        self.scorecard = kwargs.pop('scorecard', None)
        super(ScorecardKPITable, self).__init__(*args, **kwargs)
