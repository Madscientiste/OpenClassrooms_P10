from rest_framework import serializers

from .models import Comment


# created_time, is read only
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["created_time"]
