from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.conf import settings
from pathlib import Path


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='resumes/')
    name = models.CharField(max_length=255, null=True)
    mbti = models.CharField(max_length=4, null=True)
    category = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class JobDescription(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    mbti = models.CharField(max_length=4, null=True)

    def __str__(self):
        return self.title


class JobApplicationModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)
    pass
