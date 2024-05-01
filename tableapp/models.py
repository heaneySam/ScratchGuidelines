from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomGuidelines(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    external_url = models.URLField(max_length=255, blank=True, null=True)  # New field for external URL
    metadata = models.TextField(default='General')
    medical_speciality = models.CharField(max_length=255, default='General')
    def __str__(self):
        return self.name


class Trust(models.Model):
    name = models.CharField(max_length=100)

    # Add any other fields relevant to a Trust

    def __str__(self):
        return self.name

class TrustGuideline(models.Model):
    trust = models.ForeignKey(Trust, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    external_url = models.URLField(max_length=255, blank=True, null=True)  # New field for external URL
    metadata = models.TextField(default='General')
    medical_speciality = models.CharField(max_length=255, default='General')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trusts = models.ManyToManyField(Trust)
    # Add any other fields relevant to user profile

    def __str__(self):
        return self.user.username

class FavouriteGuideline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    guideline = models.ForeignKey(TrustGuideline, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        unique_together = ('user', 'guideline')  # Prevents the same guideline from being favorited multiple times by the same user

    def __str__(self):
        return f'{self.user.username} - {self.guideline.name}'
