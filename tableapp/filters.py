from django import forms
from django.db.models import Q
import django_filters
from .models import TrustGuideline
from django.db.models import Count


class TrustGuidelineFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Search")
    medical_speciality = django_filters.MultipleChoiceFilter(
        choices=TrustGuideline.objects.values_list('medical_speciality', 'medical_speciality').distinct(),
        widget=forms.CheckboxSelectMultiple
    )

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