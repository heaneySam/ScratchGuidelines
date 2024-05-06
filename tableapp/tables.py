import django_tables2 as tables
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import CustomGuidelines, TrustGuideline, FavouriteGuideline
from django_tables2.utils import A  # Alias for Accessor

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


class CustomGuidelineTable(tables.Table):
    name = tables.Column(orderable=True, verbose_name='Name')
    description = tables.Column(orderable=True, verbose_name='Description')
    selection = tables.CheckBoxColumn(accessor="pk", attrs={"th__input": {"onclick": "toggleAll(this)"}})
    delete = tables.LinkColumn('guideline_delete', args=[A('pk')], orderable=False, text='Delete',
                               attrs={"a": {"class": "btn btn-danger btn-sm"}})

    def render_name(self, record):
        if record.external_url:
            return format_html('<a href="{}" target="_blank">{}</a>', record.external_url, record.name)
        return record.name  # Return just the name if there is no URL

    class Meta:
        model = CustomGuidelines
        template_name = "django_tables2/bootstrap.html"
        fields = ("selection", "name", "description", "delete")  # Specify which fields to display
        attrs = {"class": "table table-striped table-hover"}


class TrustGuidelineTable(tables.Table):
    name = tables.Column(orderable=True, verbose_name='Name')
    description = tables.Column(orderable=True, verbose_name='Description')
    medical_speciality = tables.Column(orderable=True, verbose_name='Speciality')
    favourite = tables.Column(empty_values=(), orderable=False, verbose_name='Favourite')

    def render_name(self, record):
        if record.external_url:
            return format_html('<a href="{}" target="_blank">{}</a>', record.external_url, record.name)
        return record.name  # Return just the name if there is no URL

    def render_favourite(self, value, record):
        # Check if the user is authenticated
        if not self.request.user.is_authenticated:
            return mark_safe(
                '<span><a href="/accounts/login/" class="text-decoration-none">Login</a> to favourite</span>')

        is_favorited = FavouriteGuideline.objects.filter(user=self.request.user, guideline=record).exists()
        button_text = "Unfavourite" if is_favorited else "Favourite"
        button_class = "btn-warning" if is_favorited else "btn-primary"
        return format_html(
            '<button class="btn btn-sm {} favourite-btn" data-id="{}">{}</button>',
            button_class, record.pk, button_text
        )

    class Meta:
        model = TrustGuideline
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "description", "medical_speciality", "favourite")  # Add other fields here if needed
        attrs = {"class": "table table-striped table-hover"}


class FavouriteGuidelineTable(tables.Table):
    name = tables.Column(orderable=True, verbose_name='Name', accessor='guideline.name')
    description = tables.Column(orderable=True, verbose_name='Description', accessor='guideline.description')
    medical_speciality = tables.Column(orderable=True, verbose_name='Speciality',
                                       accessor='guideline.medical_speciality')
    unfavourite = tables.Column(empty_values=(), orderable=False, verbose_name='Unfavourite')

    def render_name(self, record):
        if record.guideline.external_url:
            return format_html('<a href="{}" target="_blank">{}</a>', record.guideline.external_url,
                               record.guideline.name)
        return record.guideline.name  # Return just the name if there is no URL

    def render_unfavourite(self, record):
        # Corrected the quotation marks around class attribute and data-id attribute
        return format_html(
            '<button class="btn btn-danger btn-sm unfavourite-btn" data-id="{}">Unfavourite</button>',
            record.guideline.id
        )

    class Meta:
        model = FavouriteGuideline
        template_name = "django_tables2/bootstrap.html"
        fields = ("name", "description", "medical_speciality", "unfavourite")
        attrs = {"class": "table table-striped table-hover"}
