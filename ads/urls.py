from django.urls import path
from .views import AdListView, AdCreateView, AdDetailView, AdUpdateView, AdDeleteView

urlpatterns = [
    path('', AdListView.as_view(), name='ad-list'),
    path('create/', AdCreateView.as_view(), name='ad-create'),
    path('<int:pk>/', AdDetailView.as_view(), name='ad-detail'),
    path('<int:pk>/update/', AdUpdateView.as_view(), name='ad-update'),
    path('<int:pk>/delete/', AdDeleteView.as_view(), name='ad-delete'),
]
