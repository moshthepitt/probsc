from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions
from easy_select2.widgets import Select2

from customers.models import Customer
from core.widgets import MiniTextarea
from core.utils import get_year_choices
from users.fields import UserModelChoiceField
from kpis.models import KPI
from .models import Scorecard, Initiative, Score


class ScoreModalForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = [
            'date',
            'value',
            'notes',
            'scorecard',
            'kpi',
        ]
        widgets = {
            'notes': MiniTextarea()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard_kpi = kwargs.pop('scorecard_kpi', None)
        super(ScoreModalForm, self).__init__(*args, **kwargs)
        if self.scorecard_kpi:
            self.fields['scorecard'].queryset = Scorecard.objects.filter(
                id__in=[self.scorecard_kpi.scorecard.pk])
            self.fields['kpi'].queryset = KPI.objects.filter(id__in=[self.scorecard_kpi.kpi.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'add-score-form'
        self.helper.layout = Layout(
            Field('date', id="id-score-date"),
            Field('value',),
            Field('notes',),
            Field('scorecard', type="hidden"),
            Field('kpi', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-block'),
            )
        )


class InitiativeModalForm(forms.ModelForm):

    class Meta:
        model = Initiative
        fields = [
            'name',
            'description',
            'date',
            'scorecard',
            'kpi',
        ]
        widgets = {
            'description': MiniTextarea()
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard_kpi = kwargs.pop('scorecard_kpi', None)
        super(InitiativeModalForm, self).__init__(*args, **kwargs)
        if self.scorecard_kpi:
            self.fields['scorecard'].queryset = Scorecard.objects.filter(
                id__in=[self.scorecard_kpi.scorecard.pk])
            self.fields['kpi'].queryset = KPI.objects.filter(id__in=[self.scorecard_kpi.kpi.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'initiative-form'
        self.helper.layout = Layout(
            Field('date', id="id-initiative-date"),
            Field('name',),
            Field('description',),
            Field('scorecard', type="hidden"),
            Field('kpi', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-block'),
            )
        )


class ScorecardForm(forms.ModelForm):
    year = forms.ChoiceField(label=_("Year"), choices=get_year_choices())

    class Meta:
        model = Scorecard
        fields = [
            'name',
            'year',
            'description',
            'user',
            'customer',
            'active',
        ]
        widgets = {
            'name': MiniTextarea(),
            'user': Select2({'width': "100%"})
        }
        field_classes = {
            'user': UserModelChoiceField
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ScorecardForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['user'].queryset = User.objects.filter(userprofile__active=True).filter(
                userprofile__customer__id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'scorecard-form'
        self.helper.layout = Layout(
            Field('name',),
            Field('year',),
            Field('user',),
            Field('description',),
            Field('customer', type="hidden"),
            Field('active',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('scorecards:scorecards_list'), _("Back")))
            )
        )
