from django import forms
from .models import CustomGuidelines, Trust

class GuidelineForm(forms.ModelForm):
    class Meta:
        model = CustomGuidelines
        fields = ['name', 'description', 'external_url', 'metadata', 'medical_speciality']

    def __init__(self, *args, **kwargs):
        super(GuidelineForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class TrustForm(forms.Form):
    trust = forms.ModelChoiceField(queryset=Trust.objects.all(), required=True, label="Select Trust", empty_label=None)
