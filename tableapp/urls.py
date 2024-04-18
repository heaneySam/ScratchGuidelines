from django.urls import path
from . import views

urlpatterns = [
  path('guidelines/',views.guideline_view, name='guideline_view'),
  path('guidelines/delete/<int:pk>/', views.delete_guideline, name='guideline_delete'),
  path('guidelines/bulk-delete/', views.bulk_delete_guidelines, name='bulk_delete_guidelines'),
]