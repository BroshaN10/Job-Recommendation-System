from django.db import models

# Create your models here.
# jobs/models.py

class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    preferences = models.TextField(blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
