from rest_framework import generics, permissions
from .models import Comment,Ad
from .serializers import CommentSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ad = Ad.objects.get(pk=self.kwargs['ad_pk'])  # Fetch Ad instance
        user = self.request.user
        if Comment.objects.filter(ad=ad, user=user).exists():
            raise PermissionDenied('You have already commented on this ad.')
        serializer.save(ad=ad, user=user)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        ad = self.kwargs['ad_pk']
        return Comment.objects.filter(ad=ad)
