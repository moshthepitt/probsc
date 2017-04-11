from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer
from strategy.models import Objective
from core.widgets import MiniTextarea
from .models import KPI


class KPIForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields = [
            'objective',
            'name',
            'measure',
            'description',
            'perspective',
            'baseline',
            'target',
            'unit',
            'direction',
            'weight',
            'reporting_period',
            'calculation',
            'reporting_method',
            'customer',
            'active',
        ]
        widgets = {
            'name': MiniTextarea(),
            'measure': MiniTextarea()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard = kwargs.pop('scorecard', None)
        super(KPIForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
        if self.scorecard:
            cancel_url = reverse('scorecards:scorecards_kpis_list', args=[self.scorecard.pk])
        else:
            cancel_url = reverse('kpis:kpis_list')
        self.fields['objective'].queryset = Objective.objects.active()
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'kpi-form'
        self.helper.layout = Layout(
            Field('name',),
            Field('measure',),
            Field('perspective',),
            Field('description',),
            Field('objective',),
            Field('baseline',),
            Field('target',),
            Field('unit',),
            Field('direction',),
            Field('weight',),
            Field('reporting_period',),
            Field('calculation',),
            Field('reporting_method', type="hidden"),
            Field('customer', type="hidden"),
            Field('active',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        cancel_url, _("Cancel")))
            )
        )

