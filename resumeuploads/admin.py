from django.contrib import admin

from .models import JobDescription


# Register your models here.
@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    exclude = ('mbti',)
    pass
