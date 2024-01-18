from rest_framework import serializers
from .models import Document


# Serializers define the API representation.
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['url', 'name', 'mbti', 'category']
