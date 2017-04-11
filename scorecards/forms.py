from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer
from core.widgets import MiniTextarea
from .models import Scorecard


class ScorecardForm(forms.ModelForm):

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

    def clean_customer(self):
        this_customer = self.cleaned_data['customer']
        if self.request:
            if not self.request.user.userprofile.customer:
                raise forms.ValidationError(_("Please select customer"))
            if this_customer != self.request.user.userprofile.customer:
                raise forms.ValidationError(_("Please select customer"))
        return this_customer

    def clean_user(self):
        this_user = self.cleaned_data['user']
        if self.request:
            if not self.request.user.userprofile.customer:
                raise forms.ValidationError(_("Please select user"))
            if this_user.userprofile.customer != self.request.user.userprofile.customer:
                raise forms.ValidationError(_("Please select user"))
        return this_user

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
            Field('customer', type="hidden"),
            Field('active',),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('scorecards:scorecards_list'), _("Cancel")))
            )
        )

