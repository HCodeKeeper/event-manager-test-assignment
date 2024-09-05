from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

EVENT_TITLE_MAX_LENGTH = 100


class Event(models.Model):
    title = models.CharField(max_length=EVENT_TITLE_MAX_LENGTH)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    location = models.TextField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    organizer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        get_user_model(), related_name="events", blank=True, through="EventToParticipant"
    )
    max_participants = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1)])

    def clean(self):
        if self.start_date < timezone.now():
            raise ValidationError({"start_date": "Start date cannot be in the past."})

        if self.end_date and self.end_date <= self.start_date:
            raise ValidationError({"end_date": "End date must be after the start date."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class EventToParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ("event", "participant")
