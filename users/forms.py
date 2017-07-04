from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions
from allauth.account.adapter import get_adapter
from allauth.account import app_settings

from customers.models import Customer
from .models import Department, Position, UserProfile
from .fields import UserModelChoiceField


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
        field_classes = {
            'manager': UserModelChoiceField
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DepartmentForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['parent'].queryset = Department.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
            self.fields['manager'].queryset = User.objects.filter(
                userprofile__customer__id=self.request.user.userprofile.customer.pk)
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
            self.fields['parent'].queryset = Position.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
            self.fields['department'].queryset = Department.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
            self.fields['supervisor'].queryset = User.objects.filter(
                userprofile__customer__id=self.request.user.userprofile.customer.pk)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'position-form'
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


class BaseUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label=_("First Name"), required=True)
    last_name = forms.CharField(label=_("Last Name"), required=True)

    class Meta:
        model = UserProfile
        fields = [
            'position',
            'customer',
            'role',
            'active'
        ]


class UserProfileForm(BaseUserProfileForm):
    email = forms.EmailField(label=_("Email Address"), required=True)

    class Meta:
        model = UserProfile
        fields = [
            'position',
            'customer',
            'role',
            'active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['customer'].queryset = Customer.objects.filter(
                id__in=[self.request.user.userprofile.customer.pk])
            self.fields['position'].queryset = Position.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'profile-form'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('position'),
            Field('role'),
            Field('active'),
            Field('customer', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('users:userprofiles_list'), _("Back")))
            )
        )

    def save(self, commit=True):
        user_profile = super(UserProfileForm, self).save(commit)
        # do custom stuff
        if self.cleaned_data['first_name']:
            user_profile.user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data['last_name']:
            user_profile.user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data['email']:
            user_profile.user.email = self.cleaned_data['email']
        user_profile.user.save()
        return user_profile


class AddUserProfileForm(BaseUserProfileForm):
    email = forms.EmailField(label=_("Email Address"), required=True)
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = UserProfile
        fields = [
            'position',
            'role',
            'active'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AddUserProfileForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user.userprofile.customer:
            self.fields['position'].queryset = Position.objects.active().filter(
                customer__id=self.request.user.userprofile.customer.pk)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.form_id = 'profile-form'
        self.helper.layout = Layout(
            Field('email'),
            Field('password'),
            Field('first_name'),
            Field('last_name'),
            Field('position'),
            Field('role'),
            Field('active'),
            FormActions(
                Submit('submitBtn', _('Submit'), css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>".format(
                        reverse('users:userprofiles_list'), _("Back")))
            )
        )

    def clean_email(self):
        value = self.cleaned_data['email']
        value = get_adapter().clean_email(value)
        if value and app_settings.UNIQUE_EMAIL:
            value = self.validate_unique_email(value)
        return value

    def validate_unique_email(self, value):
        return get_adapter().validate_unique_email(value)

    def save(self, commit=True):
        unique_username = get_adapter().generate_unique_username([
            self.cleaned_data['first_name'],
            self.cleaned_data['last_name'],
            self.cleaned_data['email'],
        ])
        user_data = dict(first_name=self.cleaned_data['first_name'],
                         last_name=self.cleaned_data['last_name'],
                         username=unique_username,
                         email=self.cleaned_data['email'],
                         password=self.cleaned_data['password'],
                         )
        user = User.objects.create_user(**user_data)
        user.userprofile.position = self.cleaned_data['position']
        user.userprofile.customer = self.request.user.userprofile.customer
        user.userprofile.role = self.cleaned_data['role']
        user.userprofile.active = self.cleaned_data['active']
        user.userprofile.save()
        return user.userprofile
