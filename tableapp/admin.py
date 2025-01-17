from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import TrustGuideline

@admin.register(TrustGuideline)
class TrustGuidelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'trust', 'viewcount', 'version_number')
    search_fields = ('name', 'description', 'medical_speciality', 'locality')
    list_filter = ('medical_speciality', 'locality', 'creation_date', 'review_date')
    ordering = ('-id',)
