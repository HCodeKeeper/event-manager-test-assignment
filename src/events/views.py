from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from events.models import Event, EventToParticipant
from events.permissions import IsEventOwner
from events.serializers import EventSerializer, RegistrationSerializer


@extend_schema(tags=["events"])
class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer(self, *args, **kwargs) -> Serializer:
        if self.action == "register":
            return RegistrationSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "add_participant"]:
            self.permission_classes = [IsEventOwner]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    @action(
        detail=False, methods=["post"], permission_classes=[IsAuthenticated], serializer_class=RegistrationSerializer
    )
    def register(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_id = serializer.validated_data["event_id"]
        event = Event.objects.get(id=event_id)

        if event.max_participants and event.participants.count() >= event.max_participants:
            return Response(
                {"message": "The event has already reached max participants number."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user == event.organizer:
            return Response({"message": "You are the organizer of the event."}, status=status.HTTP_400_BAD_REQUEST)

        EventToParticipant.objects.create(event=event, participant=user)
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
