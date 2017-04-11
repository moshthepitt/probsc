from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer
from kpis.forms import KPIForm
from kpis.models import KPI
from core.widgets import MiniTextarea
from core.utils import get_year_choices
from .models import Scorecard


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
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ScorecardForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['user'].queryset = User.objects.filter(
                userprofile__customer__id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'scorecard-form'
        self.helper.layout = Layout(
            Field('name',),
            Field('year',),
            Field('user',),
            Field('description',),
            Field('customer'),
            Field('active',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('scorecards:scorecards_list'), _("Cancel")))
            )
        )


class KPIFormSetHelper(FormHelper):

    def __init__(self, *args, **kwargs):
        super(KPIFormSetHelper, self).__init__(*args, **kwargs)
        self.form_tag = False
        self.form_method = 'post'
        self.template = 'bootstrap3/table_inline_formset.html'


class BaseKPIFormSet(forms.BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super(BaseKPIFormSet, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            scorecard_instance = kwargs['instance']
            for form in self.forms:
                if 'customer' in form.fields:
                    form.fields['customer'].queryset = Customer.objects.filter(
                        customer=scorecard_instance.customer)


KPIFormSet = inlineformset_factory(Scorecard, KPI, form=KPIForm, formset=BaseKPIFormSet, can_delete=True, extra=5)
