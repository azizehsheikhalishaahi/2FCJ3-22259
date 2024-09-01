from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'ad', 'text', 'created_at']
        read_only_fields = ['ad', 'user', 'created_at']
