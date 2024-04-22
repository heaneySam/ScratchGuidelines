from django import forms
from .models import CustomGuidelines

class GuidelineForm(forms.ModelForm):
    class Meta:
        model = CustomGuidelines
        fields = ['name', 'description', 'external_url', 'metadata', 'medical_speciality']

    def __init__(self, *args, **kwargs):
        super(GuidelineForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
