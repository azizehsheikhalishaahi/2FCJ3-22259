from rest_framework import generics
from .models import Ad
from .serializers import AdSerializer
from rest_framework import permissions

class AdPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class AdListCreateView(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AdRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [AdPermission]

class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]  
