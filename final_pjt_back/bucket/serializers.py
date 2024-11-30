from rest_framework import serializers
from .models import Bucket

class BucketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bucket
        fields = ['user', 'product']
