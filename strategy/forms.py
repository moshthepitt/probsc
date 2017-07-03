from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer
from .models import StrategicTheme, Objective


class StrategicThemeForm(forms.ModelForm):

    class Meta:
        model = StrategicTheme
        fields = ['name', 'description', 'customer', 'active']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StrategicThemeForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'strategic-theme-form'
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('active'),
            Field('customer', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('strategy:strategic_themes_list'), _("Back")))
            )
        )


class ObjectiveForm(forms.ModelForm):

    class Meta:
        model = Objective
        fields = [
            'name',
            'description',
            'strategic_theme',
            'parent',
            'customer',
            'active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ObjectiveForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['strategic_theme'].queryset = StrategicTheme.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
            self.fields['parent'].queryset = Objective.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'objective-form'
        self.helper.layout = Layout(
            Field('name'),
            Field('strategic_theme'),
            Field('parent'),
            Field('description'),
            Field('active'),
            Field('customer', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('strategy:objectives_list'), _("Back")))
            )
        )

