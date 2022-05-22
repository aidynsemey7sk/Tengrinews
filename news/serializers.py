from rest_framework import serializers
from .models import Category, Post, PostImage
from django.contrib.auth.models import User


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = (
            'image',
        )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', ]


# class CommentSerializer(serializers.ModelSerializer):
#     owner = UserSerializer()
#
#     class Meta:
#         model = Comment
#         fields = ['id', 'body', 'owner',  'post']


class PostSerializer(serializers.ModelSerializer):
    image_for_post = PostImageSerializer(many=True)
    # comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "get_absolute_url",
            "text",
            "get_image",
            "get_thumbnail",
            'image_for_post',
            'date_added',
            'slug',
            'view_count',
            'get_date',

            # 'comments',
        )


class CategorySerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "posts",
        )
