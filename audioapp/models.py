from datetime import datetime

import pytz
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models


# DateTime Validator.
def validate_datetime(uploaded_time):
    print(uploaded_time, datetime.now(pytz.timezone('Asia/Kolkata')))
    if uploaded_time < datetime.now(pytz.timezone('Asia/Kolkata')):
        raise ValidationError("DateTime cannot be in the past")


# Song Model.
class Song(models.Model):
    name = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank=False)
    uploaded_time = models.DateTimeField(default=datetime.now, blank=False, validators=[validate_datetime])


# Podcast Model.
class Podcast(models.Model):
    name = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank=False)
    uploaded_time = models.DateTimeField(default=datetime.now, blank=False, validators=[validate_datetime])
    host = models.CharField(max_length=100, blank=False)
    participants = ArrayField(models.CharField(max_length=100), max_length=10, blank=True)


# Audiobook Model.
class Audiobook(models.Model):
    title = models.CharField(max_length=100, blank=False)
    author = models.CharField(max_length=100, blank=False)
    narrator = models.CharField(max_length=100, blank=False)
    duration = models.PositiveIntegerField(blank=False)
    uploaded_time = models.DateTimeField(default=datetime.now, blank=False, validators=[validate_datetime])
