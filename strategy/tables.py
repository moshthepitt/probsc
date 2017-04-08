from django.utils.html import format_html
from django.utils.translation import ugettext as _

import django_tables2 as tables

from .models import StrategicTheme


class StrategicThemeTable(tables.Table):
    action = tables.Column(verbose_name="", accessor='pk', orderable=False)
    active = tables.BooleanColumn(
        attrs={
            'td': {'class': "not-active"},
            'th': {'class': "not-active"}
        }
    )

    class Meta:
        model = StrategicTheme
        exclude = ['created', 'modified', 'description', 'id', 'customer']
        sequence = ('name', 'active', '...')
        empty_text = _("Nothing to show")
        template = "django_tables2/bootstrap.html"
        # per_page = 1
        # attrs = {'class': 'paleblue'}  # add class="paleblue" to <table> tag

    def render_action(self, record):
        return format_html('<a href="{}">Edit</a>', record.get_edit_url())
