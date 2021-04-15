from rest_framework import serializers
import json

from core.models import Sample

class SampleSerializer(serializers.ModelSerializer):

    # def to_representation(self, data):
    #     """
    #     Override super method to represent data nested objects from OrderedDict to Dict
    #     """
    #     res = super(SampleSerializer, self).to_representation(data)
    #     full_entry = json.loads(json.dumps(res))

    #     return full_entry

    class Meta:
        model = Sample
        fields = '__all__'