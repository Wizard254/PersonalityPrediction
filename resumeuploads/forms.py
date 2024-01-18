from django import forms
from .models import Document, JobDescription


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)


class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = JobDescription
        fields = ('description', 'title', 'category',)
