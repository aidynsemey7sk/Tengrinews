from django.db.models import Q
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from datetime import datetime, timedelta

last_hours = datetime.now() - timedelta(hours=24)


# Все посты для главной страницы
class AllPostsList(APIView):
    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


# Посты для карточек в центре
class LatestPostsList(APIView):
    def get(self, request, format=None):
        post = Post.objects.all()[0:6]
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


class ReadPostList(APIView):
    def get(self, request, format=None):
        post = Post.objects.filter(category__name='article')
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


# Поста для главной новости выбирается по дате и большему количеству просмотров
class TopViewPost(APIView):
    def get(self, request, format=None):
        top_view_post = Post.objects.filter(
            date_added__gte=last_hours).order_by('-view_count').first()
        if top_view_post:
            serializer = PostSerializer(top_view_post)
            return Response(serializer.data)
        else:
            top_view_post = Post.objects.all().order_by('-view_count').first()
            print(top_view_post.get_date)
            serializer = PostSerializer(top_view_post)
            return Response(serializer.data)


# Детали поста, подсчитывает количество просмотров
# class PostDetail(APIView):
#     def get_object(self, category_slug, post_slug):
#         try:
#             post = Post.objects.filter(
#                 category__slug=category_slug).get(slug=post_slug)
#             post.view_count = post.view_count + 1
#             post.save()
#             return Post.objects.filter(
#                 category__slug=category_slug).get(slug=post_slug)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def get(self, request, category_slug, post_slug, format=None):
#         post = self.get_object(category_slug, post_slug)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def retrieve(self, request, *args, **kwargs):
#         obj = self.get_object()
#         obj.view_count = obj.view_count + 1
#         obj.save(update_fields=("view_count",))
#         return super().retrieve(request, *args, **kwargs)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)


# class CommentsList(APIView):
#     def get(self, request, format=None):
#         post = Comment.objects.all()
#         serializer = CommentSerializer(post, many=True)
#         return Response(serializer.data)


