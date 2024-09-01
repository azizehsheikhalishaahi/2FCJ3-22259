from django.urls import path
from .views import AdListCreateView, AdRetrieveUpdateDestroyView

urlpatterns = [
    path('', AdListCreateView.as_view(), name='ad-list-create'),  # For listing and creating ads
    path('<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='ad-detail'),  # For retrieving, updating, and deleting ads
]
