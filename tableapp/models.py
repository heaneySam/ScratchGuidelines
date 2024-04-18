from django.db import models

# Create your models here.
class Guideline(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    external_url = models.URLField(max_length=255, blank=True, null=True)  # New field for external URL
    metadata = models.TextField(default='General')
    medical_speciality = models.CharField(max_length=255, default='General')
    def __str__(self):
        return self.name
