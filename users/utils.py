from django.forms import ModelChoiceField


class UserModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.userprofile:
            return obj.userprofile.get_name()
        return obj.get_full_name()
