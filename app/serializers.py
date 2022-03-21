from rest_framework import serializers
from .models import Project

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ("projectName", "file", "fileExt")



