from django import forms
from django.db.models import Q
import django_filters
from django.urls import reverse_lazy

from .models import TrustGuideline, Trust
from django.db.models import Count


class TrustGuidelineFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Search")
    # medical_speciality = django_filters.MultipleChoiceFilter(
    #     choices=TrustGuideline.objects.values_list('medical_speciality', 'medical_speciality').distinct(),
    #     widget=forms.CheckboxSelectMultiple
    # )
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
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    class Meta:
        model = TrustGuideline
        fields = ['search', 'medical_speciality']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        speciality_choices = TrustGuideline.objects.values('medical_speciality').annotate(
            count=Count('medical_speciality')
        ).order_by('-count')

        self.filters['medical_speciality'].extra['choices'] = [
            (s['medical_speciality'], f"{s['medical_speciality']} ({s['count']})")
            for s in speciality_choices
        ]