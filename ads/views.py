from rest_framework import generics
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from .models import Ad
from .serializers import AdSerializer

class AdListView(generics.ListAPIView):
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]

class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.AllowAny]

class AdUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        ad = super().get_object()
        if ad.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this ad.")
        return ad

class AdDeleteView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        ad = super().get_object()
        if ad.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this ad.")
        return ad