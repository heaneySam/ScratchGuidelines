from django import forms
from .models import Guideline

class GuidelineForm(forms.ModelForm):
    class Meta:
        model = Guideline
        fields = ['name', 'description', 'external_url', 'metadata', 'medical_speciality']

    def __init__(self, *args, **kwargs):
        super(GuidelineForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False
