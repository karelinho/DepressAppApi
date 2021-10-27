from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Depress(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sleep = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    headache = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    tiredness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    appetite = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    constipation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    self_blame_thoughts = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    mood = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    self_destructive_thoughts = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    concentration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    physical_discomfort = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    tense_feeling = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])
    sleep_length = models.TextField(default='0', max_length=256, blank=True)
