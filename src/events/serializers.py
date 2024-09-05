from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from events.models import Event


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name"]


class EventSerializer(serializers.ModelSerializer):
    # Participants Can cause perf issues if there are many participants
    participants = ParticipantSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "start_date",
            "end_date",
            "location",
            "max_participants",
            "organizer",
            "participants",
            "participant_count",
        ]
        read_only_fields = ["id", "participant_count", "organizer"]

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate(self, data):
        """
        Check that the start_date is before the end_date.
        """
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("The start date must be before the end date.")
        return data

    def validate_start_date(self, data):
        if data < timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past.")
        return data

    def validate_end_date(self, data):
        if data <= timezone.now():
            raise serializers.ValidationError("End date must be after the start date.")
        return data


class RegistrationSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()

    def validate_event_id(self, value):
        if not Event.objects.filter(id=value).exists():
            raise serializers.ValidationError("Event with this ID does not exist.")
        return value
