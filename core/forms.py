from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import Field, FieldWithButtons


class ListViewSearchForm(forms.Form):
    name = forms.CharField(label=_("Name"), required=False)

    def __init__(self, *args, **kwargs):
        super(ListViewSearchForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'get'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.html5_required = True
        self.helper.form_id = 'search-form'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.layout = Layout(
            FieldWithButtons(
                Field('name', css_class="input-sm"),
                Submit('submitBtn', _('Search'), css_class='btn-sm')
            ),
        )
