from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class CustomGuidelines(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()
    external_url = models.URLField(max_length=1024, blank=True, null=True)  # New field for external URL
    metadata = models.TextField(default='General')
    medical_speciality = models.CharField(max_length=1024, default='General')

    def __str__(self):
        return self.name


class Trust(models.Model):
    name = models.CharField(max_length=100)

    # Add any other fields relevant to a Trust

    def __str__(self):
        return self.name


class TrustGuideline(models.Model):
    trust = models.ForeignKey(Trust, on_delete=models.CASCADE)
    name = models.CharField(max_length=1025)
    description = models.TextField()
    external_url = models.URLField(max_length=1025, blank=True, null=True)
    metadata = models.TextField(default='General')
    medical_speciality = models.CharField(max_length=255, default='General')
    locality = models.CharField(max_length=255, default='UHD')
    original_filename = models.CharField(max_length=1025, default='null')
    viewcount = models.IntegerField(default=0, db_index=True)  # New field to track views
    version_number = models.CharField(max_length=255, default='0', db_index=True)  # Changed to CharField
    authors = models.CharField(max_length=1025, blank=True, null=True)  # New field for authors
    creation_date = models.CharField(max_length=255, blank=True, null=True)  # New field for creation date
    review_date = models.CharField(max_length=255, blank=True, null=True)  # New field for review date


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
        unique_together = (
        'user', 'guideline')  # Prevents the same guideline from being favorited multiple times by the same user

    def __str__(self):
        return f'{self.user.username} - {self.guideline.name}'
