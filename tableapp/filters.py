from django import forms
from django.db.models import Q
import django_filters
from django.urls import reverse_lazy

from .models import TrustGuideline, Trust
from django.db.models import Count


class TrustGuidelineFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Search")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )

    class Meta:
        model = TrustGuideline
        fields = ['search']

