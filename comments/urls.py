from django.urls import path
from .views import CommentCreateView, CommentListView

urlpatterns = [
    path('ads/<int:ad_pk>/', CommentListView.as_view(), name='comment-list'),
    path('ads/<int:ad_pk>/add/', CommentCreateView.as_view(), name='comment-create'),
]
