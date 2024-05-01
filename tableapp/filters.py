from django import forms
from django.db.models import Q
import django_filters
from django.urls import reverse, reverse_lazy
from .models import TrustGuideline, Trust

class TrustGuidelineFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Search", widget=forms.TextInput(attrs={
        'hx-trigger': 'keyup changed delay:500ms clear:none from:input',
        'hx-target': '#table-container',  # Make sure this ID matches the container in your HTML
        'hx-get': reverse_lazy('trust_guideline_view'),
        'class': 'form-control',
        'placeholder': 'Search names and descriptions...'
    }))
    trust = django_filters.ModelChoiceFilter(queryset=Trust.objects.all(), empty_label=None, widget=forms.Select(attrs={
        'hx-get': reverse_lazy('trust_guideline_view'),
        'hx-trigger': 'change',  # This will trigger the filter when the dropdown changes
        'hx-target': '#table-container',
        'class': 'form-control'
    }))

    def __init__(self, *args, **kwargs):
        super(TrustGuidelineFilter, self).__init__(*args, **kwargs)
        # Set default trust if not provided by the user
        if 'trust' not in self.data:
            # Select a default trust, can be dynamic based on conditions
            default_trust = Trust.objects.first()  # or any other logic to select a default trust
            self.form.fields['trust'].initial = default_trust
            self.queryset = self.queryset.filter(trust=default_trust)



    def filter_search(self, queryset, name, value):
        """
        This method will be used to filter the queryset based on the 'name' and 'description' fields.
        """
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    class Meta:
        model = TrustGuideline
        fields = []
