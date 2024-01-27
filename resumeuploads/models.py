import dataclasses

# Create your models here.
from django.contrib.auth.models import User
from django.db import models


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
    resume = models.ForeignKey(Document, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    class Meta:
        unique_together = ['user', 'job', 'resume']
        pass

    @dataclasses.dataclass
    class Status:
        WAITING: int = 1
        SUCCESS: int = 2
        DECLINED: int = 3
        pass
    pass
