from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from custom_users.serializers import UserSerializer


@extend_schema(tags=["users"])
class UserViewSet(viewsets.GenericViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


@extend_schema(tags=["users"])
class MeView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request):
        return super().retrieve(request)
