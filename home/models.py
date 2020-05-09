from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Event(models.Model):
    name = models.TextField(max_length=255)
    time = models.DateTimeField(auto_now=False, auto_now_add=False)
    timeslot_in_mins = models.IntegerField()

class EventToken(models.Model):
    event_id = models.ForeignKey("Event", on_delete = models.CASCADE)
    token_id = models.IntegerField()
    timing = models.TimeField(auto_now=False, auto_now_add=False)
    username = models.TextField(max_length=255)

