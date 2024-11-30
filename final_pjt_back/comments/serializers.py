from rest_framework import serializers
from .models import Comment
from django.contrib.auth import get_user_model

class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source='user.nickname', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    tier = serializers.CharField() 
    class Meta:
        model = Comment
        fields = ['id', 'nickname', 'content', 'created_at', 'user_id','tier']