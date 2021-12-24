from rest_framework.permissions import AllowAny
from rest_framework import generics

from users.models import User

from .serializers import RegisterUserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer
