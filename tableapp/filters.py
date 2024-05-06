from django import forms
from django.db.models import Q
import django_filters
from django.urls import reverse, reverse_lazy
from .models import TrustGuideline, Trust

class TrustGuidelineFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label="Search")

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
