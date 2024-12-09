from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.views import APIView
from datetime import datetime

class BlogPostListCreate(generics.ListCreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer

    def delete(self, request, *args, **kwargs):
        BlogPost.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk"

class BlogPostList(APIView):
    def get(self, request, formate=None):
        title = request.query_params.get("title", "")
        published_date = request.query_params.get("published_date", "")

        if published_date:
            try:
                published_date = datetime.strptime(published_date, "%m-%d-%Y").date()
            except ValueError:
                return Response({"error": "Invalid date format. Please use MM-DD-YYYY."}, status=status.HTTP_400_BAD_REQUEST)


        if title and published_date:
            blog_posts = BlogPost.objects.filter(title__icontains=title, published_date__date=published_date)
        elif title:
            blog_posts = BlogPost.objects.filter(title__icontains=title)
        elif published_date:
            blog_posts = BlogPost.objects.filter(published_date__date=published_date)
        else:
            blog_posts = BlogPost.objects.all()

        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)