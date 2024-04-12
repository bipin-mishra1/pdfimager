from rest_framework import serializers
from .models import ImageZipFile


class PDFFileSerializer(serializers.Serializer):
    pdf_file = serializers.FileField()


class ImageZipFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageZipFile
        fields = '__all__'
