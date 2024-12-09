from rest_framework import serializers
from .models import BlogPost

class BlogPostSerializer(serializers.ModelSerializer):
    published_date = serializers.DateTimeField(format="%d-%m-%Y")

    class Meta:
        model = BlogPost
        fields = ["id", "title", "content", "published_date"]