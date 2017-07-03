from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions

from customers.models import Customer
from .models import Department, Position


class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = [
            'name',
            'parent',
            'manager',
            'description',
            'customer',
            'active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DepartmentForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'department-form'
        self.helper.layout = Layout(
            Field('name'),
            Field('parent'),
            Field('manager'),
            Field('description'),
            Field('active'),
            Field('customer', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('users:departments_list'), _("Back")))
            )
        )


class PositionForm(forms.ModelForm):

    class Meta:
        model = Position
        fields = [
            'name',
            'parent',
            'department',
            'supervisor',
            'description',
            'customer',
            'active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(PositionForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'department-form'
        self.helper.layout = Layout(
            Field('name'),
            Field('department'),
            Field('parent'),
            Field('supervisor'),
            Field('description'),
            Field('active'),
            Field('customer', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('users:positions_list'), _("Back")))
            )
        )
