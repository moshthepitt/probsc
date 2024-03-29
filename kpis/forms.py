from decimal import Decimal

from django import forms
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions
from easy_select2.widgets import Select2

from customers.models import Customer
from strategy.models import Objective
from core.widgets import MiniTextarea
from scorecards.models import ScorecardKPI
from kpis.models import KPI


def clean_weight_func(value, kpi, scorecard):
    """
    ensure that the total weight values are not more than 100%
    """
    if scorecard:
        try:
            scorecard_kpis = ScorecardKPI.objects.filter(scorecard=scorecard)
        except ScorecardKPI.DoesNotExist:
            pass
        else:
            if kpi and kpi.id:
                # this kpi already exists
                # we remove it from the queryset so that its weight
                # is not summed up below
                scorecard_kpis = scorecard_kpis.exclude(kpi=kpi)

            sum_dict = scorecard_kpis.aggregate(
                            weight_sum=Coalesce(Sum('kpi__weight'), Value(0)))
            # sum of all weights in the scorecard, excluding the
            # current one
            weight_sum = sum_dict['weight_sum']
            # ensure that the sums does not go above 100%
            if (value + weight_sum) > Decimal(100):
                raise forms.ValidationError(
                    _('The sum of the weights in a Scorecard cannot exceed'
                      ' 100%.  Please reduce the value of this weight, or'
                      ' of other weights in this scorecard.'))


def clean_customer_func(value, scorecard):
    """
    ensure that the customer is set properly
    """
    if scorecard:
        if value != scorecard.customer:
            raise forms.ValidationError(_("Wrong Customer"))
    return value


class KPIForm(forms.ModelForm):
    """
    generic scorecard kpi form
    """

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
            'measure': MiniTextarea(),
            'objective': Select2({'width': "100%"})
        }

    def clean_weight(self):
        value = self.cleaned_data['weight']
        # ensure that the sum of weights in a scorecard <= 100
        clean_weight_func(value, self.instance, self.scorecard)
        return value

    def clean_customer(self):
        """
        ensure that the customer is set properly
        """
        value = self.cleaned_data['customer']
        clean_customer_func(value, self.scorecard)
        return value

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard = kwargs.pop('scorecard', None)
        super(KPIForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['objective'].queryset =\
                Objective.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
        if self.scorecard:
            cancel_url = reverse('scorecards:scorecards_kpis_list', args=[
                self.scorecard.pk])
        else:
            cancel_url = reverse('kpis:kpis_list')
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
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
                Submit('submitBtn', _('Submit'), css_class='btn-success '
                                                           'btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(cancel_url, _("Back")))
            )
        )


class UserKPIForm(forms.ModelForm):
    """
    Used when the user is editting their own scorecard KPIs
    """

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
            'measure': MiniTextarea(),
            'objective': Select2({'width': "100%"})
        }

    def clean_weight(self):
        value = self.cleaned_data['weight']
        # ensure that the sum of weights in a scorecard <= 100
        clean_weight_func(value, self.instance, self.scorecard)
        return value

    def clean_customer(self):
        """
        ensure that the customer is set properly
        """
        value = self.cleaned_data['customer']
        clean_customer_func(value, self.scorecard)
        return value

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard = kwargs.pop('scorecard', None)
        super(UserKPIForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['objective'].queryset =\
                Objective.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
        cancel_url = reverse('scorecards:user_scorecards_kpis_list', args=[
            self.scorecard.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
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
                Submit('submitBtn', _('Submit'), css_class='btn-success '
                                                           'btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(cancel_url, _("Back")))
            )
        )
