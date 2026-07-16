from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class UserHealthProfile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    age        = models.IntegerField(null=True, blank=True)
    height     = models.FloatField(null=True, blank=True)
    weight     = models.FloatField(null=True, blank=True)
    goal       = models.CharField(max_length=50, null=True, blank=True)
    gender     = models.CharField(max_length=20, blank=True, default='')
    activity   = models.CharField(max_length=50, blank=True, default='')
    diet       = models.CharField(max_length=50, blank=True, default='')
    conditions = models.TextField(blank=True, default='')

    def __str__(self):
        return self.user.username


class FitnessLog(models.Model):
    MOOD_CHOICES = [
        (1, '😞 Terrible'),
        (2, '😕 Bad'),
        (3, '😐 Okay'),
        (4, '😊 Good'),
        (5, '🔥 Amazing'),
    ]
    INTENSITY_CHOICES = [
        ('low',    'Low'),
        ('medium', 'Medium'),
        ('high',   'High'),
    ]
    WORKOUT_CHOICES = [
        ('running',  '🏃 Running'),
        ('cycling',  '🚴 Cycling'),
        ('weights',  '🏋️ Weights'),
        ('swimming', '🏊 Swimming'),
        ('yoga',     '🧘 Yoga'),
        ('hiit',     '⚡ HIIT'),
        ('walking',  '🚶 Walking'),
        ('rest',     '😴 Rest Day'),
        ('other',    '🎯 Other'),
    ]

    user      = models.ForeignKey(User, on_delete=models.CASCADE)
    date      = models.DateField(default=timezone.now)
    weight    = models.FloatField(null=True, blank=True)
    calories  = models.IntegerField(null=True, blank=True)
    steps     = models.IntegerField(null=True, blank=True)
    water     = models.FloatField(null=True, blank=True)
    
    workout   = models.CharField(max_length=50, choices=WORKOUT_CHOICES, blank=True)
    duration  = models.IntegerField(null=True, blank=True)
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES, blank=True)
    mood      = models.IntegerField(choices=MOOD_CHOICES, null=True, blank=True)
    notes     = models.TextField(blank=True)
    created   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"