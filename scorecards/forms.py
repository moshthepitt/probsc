from django import forms
from django.utils.translation import ugettext as _
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML
from crispy_forms.bootstrap import Field, FormActions, FieldWithButtons
from easy_select2.widgets import Select2

from customers.models import Customer
from core.widgets import MiniTextarea
from core.utils import get_year_choices
from users.fields import UserModelChoiceField
from users.models import Department
from kpis.models import KPI
from scorecards.models import Scorecard, Initiative, Score, Evidence


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

    def clean(self):
        cleaned_data = super(ScoreModalForm, self).clean()
        scorecard = cleaned_data.get("scorecard")
        kpi = cleaned_data.get("kpi")
        if kpi:
            max_scores = kpi.get_number_of_scores()
            num_scores = Score.objects.filter(
                scorecard=scorecard, kpi=kpi).count()
            if num_scores + 1 > max_scores:
                msg = _("Cannot add more scores.".format())
                self.add_error('date', msg)
                self.add_error('value', msg)
                self.add_error('notes', msg)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard_kpi = kwargs.pop('scorecard_kpi', None)
        super(ScoreModalForm, self).__init__(*args, **kwargs)
        if self.scorecard_kpi:
            self.fields['scorecard'].queryset = Scorecard.objects.filter(
                id__in=[self.scorecard_kpi.scorecard.pk])
            self.fields['kpi'].queryset = KPI.objects.filter(
                id__in=[self.scorecard_kpi.kpi.pk])
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
                Submit('submitBtn',
                       _('Submit'),
                       css_class='btn-success btn-block'),
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
            self.fields['kpi'].queryset = KPI.objects.filter(
                id__in=[self.scorecard_kpi.kpi.pk])
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
                Submit('submitBtn',
                       _('Submit'),
                       css_class='btn-success btn-block'),
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
            self.fields['user'].queryset = User.objects.filter(
                userprofile__active=True).filter(
                userprofile__customer__id__in=[
                    self.request.user.userprofile.customer.pk])
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
                Submit('submitBtn', _('Submit'), css_class='btn-success '
                                                           'btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(
                        reverse('scorecards:scorecards_list'), _("Back")))
            )
        )


class UserScorecardForm(forms.ModelForm):
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
        super(UserScorecardForm, self).__init__(*args, **kwargs)
        if self.request and self.request.user:
            self.fields['user'].queryset = User.objects.filter(
                id__in=[self.request.user.id])
            if self.request.user.userprofile.customer:
                self.fields['customer'].queryset = Customer.objects.filter(
                    id__in=[self.request.user.userprofile.customer.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'user_scorecard-form'
        self.helper.layout = Layout(
            Field('name',),
            Field('year',),
            Field('user',),
            Field('description',),
            Field('customer', type="hidden"),
            Field('active',),
            FormActions(
                Submit('submitBtn',
                       _('Submit'),
                       css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(
                        reverse('scorecards:user_scorecards'), _("Back")))
            )
        )


class ScorecardApprovalForm(forms.ModelForm):

    class Meta:
        model = Scorecard
        fields = [
            'approved',
            'approved_by',
            'approval_note'
        ]
        widgets = {
            'approval_note': MiniTextarea(),
            'approved_by': Select2({'width': "100%"})
        }
        field_classes = {
            'approved_by': UserModelChoiceField
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ScorecardApprovalForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields['approved_by'].queryset = User.objects.filter(
                id__in=[self.request.user.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'scorecard-approval-form'
        self.helper.layout = Layout(
            Field('approved',),
            Field('approved_by',),
            Field('approval_note',),
            FormActions(
                Submit('submitBtn',
                       _('Submit'),
                       css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(
                        reverse('scorecards:scorecards_list'), _("Back")))
            )
        )


class StaffScorecardApprovalForm(forms.ModelForm):

    class Meta:
        model = Scorecard
        fields = [
            'approved',
            'approved_by',
            'approval_note'
        ]
        widgets = {
            'approval_note': MiniTextarea(),
            'approved_by': Select2({'width': "100%"})
        }
        field_classes = {
            'approved_by': UserModelChoiceField
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(StaffScorecardApprovalForm, self).__init__(*args, **kwargs)
        self.instance = kwargs.get('instance', None)
        if self.request:
            self.fields['approved_by'].queryset = User.objects.filter(
                id__in=[self.request.user.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'scorecard-approval-form'
        self.helper.layout = Layout(
            Field('approved',),
            Field('approved_by',),
            Field('approval_note',),
            FormActions(
                Submit('submitBtn',
                       _('Submit'),
                       css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    "".format(
                        reverse('scorecards:staff_scorecards',
                                args=[self.instance.user.pk]),
                        _("Back")))
            )
        )


class EvidenceForm(forms.ModelForm):

    class Meta:
        model = Evidence
        fields = [
            'scorecard',
            'name',
            'date',
            'file'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.scorecard = kwargs.pop('scorecard', None)
        super(EvidenceForm, self).__init__(*args, **kwargs)
        cancel_url = reverse('scorecards:scorecard_evidence_list',
                             args=[self.scorecard.pk])
        self.fields['scorecard'].queryset = Scorecard.objects.filter(
            id__in=[self.scorecard.pk])
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'evidence-form'
        self.helper.layout = Layout(
            Field('name',),
            Field('date',),
            Field('file',),
            Field('scorecard', type="hidden"),
            FormActions(
                Submit('submitBtn', _('Submit'),
                       css_class='btn-success btn-250'),
                HTML(
                    "<a class='btn btn-default btn-250' href='{}'>{}</a>"
                    .format(cancel_url, _("Back")))
            )
        )

    def clean_file(self):
        value = self.cleaned_data['file']
        if value.content_type not in settings.ALLOWED_UPLOADS:
            raise forms.ValidationError(_('You can only upload PDF, Word '
                                          'and/or Excel files.'))
        if value._size > settings.MAX_UPLOAD_SIZE:
            raise forms.ValidationError(_('Maximum file upload size is 5MB.'))
        return value


class ScorecardListViewSearchForm(forms.ModelForm):
    q = forms.CharField(label=_("Search Query"), required=False)
    year = forms.ChoiceField(
            label=_("Year"), required=False,
            widget=Select2(select2attrs={'width': '170',
                                         'placeholder': _('Year')}),
            choices=[(x, x) for x in range(2012, 3000)])
    approved = forms.ChoiceField(
                label=_("Approved"), required=False,
                choices=[(None, ""), (True, _("Yes")), (False, _("No"))],
                widget=Select2(select2attrs={'width': '170',
                                             'placeholder': _('Approved')}))
    user__userprofile__position__department = forms.ModelChoiceField(
        label=_("Department"), required=False, widget=Select2(
            select2attrs={'width': '170', 'placeholder': _('Department')}),
        queryset=Department.objects.all())

    class Meta:
        model = Scorecard
        fields = ['year', 'approved']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ScorecardListViewSearchForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields['user__userprofile__position__department'].queryset = Department.objects.filter(customer=self.request.user.userprofile.customer)  # noqa
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'get'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'search-form'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            Field('user__userprofile__position__department',
                  css_class="input-sm"),
            Field('approved', css_class="input-sm"),
            Field('year', css_class="input-sm"),
            FieldWithButtons(
                Field('q', css_class="input-sm"),
                Submit('submitBtn', _('Filter'), css_class='btn-sm')
            ),
        )
