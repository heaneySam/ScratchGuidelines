from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    TrustGuidelineViewSet,
    TestAPI,
    TrustGuidelineListAPIView,
    TrustGuidelineAllAPIView,
    TrustGuidelineAllMinimalAPIView,
)

router = DefaultRouter()
router.register(r'trustguidelines', TrustGuidelineViewSet)

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
    path('api/test/', TestAPI.as_view(), name='test-api'),
    path('api/', include(router.urls)),
    path('api/trust-guidelines/', TrustGuidelineListAPIView.as_view(), name='trust_guideline_list'),
    path('api/trust-guidelines/all/', TrustGuidelineAllAPIView.as_view(), name='trust_guideline_all'),
    path('api/trust-guidelines/all-minimal/', TrustGuidelineAllMinimalAPIView.as_view(), name='trust_guideline_all_minimal'),
    path('api/trust-guidelines/<int:pk>/', views.TrustGuidelineRetrieveAPIView.as_view(), name='trust_guideline_retrieve'),
    path('api/trust-guidelines/<int:pk>/update/', views.TrustGuidelineUpdateAPIView.as_view(), name='trust_guideline_update'),

]