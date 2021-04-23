import json

from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from rest_framework import serializers
from apps.core.models import CsvFile


class UploadCsvSerializer(serializers.ModelSerializer):
    token = serializers.CharField(write_only=True)
    file = serializers.FileField()

    class Meta:
        model = CsvFile
        fields = '__all__'


class CsvFileSerializer(serializers.ModelSerializer):
    file = serializers.URLField(read_only=True)

    class Meta:
        model = CsvFile
        fields = '__all__'


class UploadCsvSerializer(serializers.Serializer):
    file = serializers.FileField()

    def create(self, validated_data):
        # get user       
        user_obj = User.objects.get(id=self.context['user'].id)
        # save file on storage
        file_path = default_storage.save(validated_data['file'].name, validated_data['file'])
        # add file on model and link with user
        CsvFile.objects.create(user=user_obj, file=file_path)
        file_obj = CsvFile.objects.get(file=file_path)
        file_serialized = CsvFileSerializer(file_obj).data
        return file_serialized
