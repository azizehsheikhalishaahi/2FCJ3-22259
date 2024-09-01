from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import SignupSerializer, LoginSerializer, LogoutSerializer

class SignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()
        return Response({"token": token.key}, status=status.HTTP_200_OK)


# class LogoutView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         # Try to find and delete the token
#         try:
#             token = Token.objects.get(user=request.user)
#             token.delete()
#         except Token.DoesNotExist:
#             # Token does not exist
#             return Response({"detail": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(status=status.HTTP_204_NO_CONTENT)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if not request.user.auth_token:
            return Response(status=status.HTTP_400_BAD_REQUEST)  # Return 400 if no token is found
        
        request.user.auth_token.delete()  # Delete the token
        return Response(status=status.HTTP_204_NO_CONTENT)