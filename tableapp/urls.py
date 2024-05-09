from django.urls import path
from . import views

urlpatterns = [
  path('', views.TrustGuidelineListView.as_view(), name='trust_guideline_view'),
  path('guidelines/',views.guideline_view, name='guideline_view'),
  path('guidelines/delete/<int:pk>/', views.delete_guideline, name='guideline_delete'),
  path('guidelines/bulk-delete/', views.bulk_delete_guidelines, name='bulk_delete_guidelines'),
  path('trustGuidelines/',views.TrustGuidelineListView.as_view(), name='trust_guideline_view'),
  path('add-to-favourites/<int:pk>/', views.add_to_favourites, name='add_to_favourites'),
  path('unfavourite/<int:pk>/', views.unfavourite_guideline, name='unfavourite_guideline'),
  path('favouriteGuidelines/', views.favourite_guideline_view, name='favourite_guideline_view'),
  path('guidelines/view_pdf/<int:pk>/', views.RedirectAndCountView.as_view(), name='view_pdf'),

]