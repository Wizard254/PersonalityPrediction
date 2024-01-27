from rest_framework import serializers
from resumeuploads.models import JobDescription, Document


# Serializers define the API representation.
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'mbti', 'category']


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        # fields = ['url', 'username', 'email', 'groups']
        fields = ['title', 'category', 'description']
        pass
    pass
