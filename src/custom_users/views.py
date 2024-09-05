from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from custom_users.serializers import UserSerializer


@extend_schema(tags=["Users"])
class UserView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["Users"])
class MeView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request):
        return super().retrieve(request)
