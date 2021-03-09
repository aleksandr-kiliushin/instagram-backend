from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Comment, Post, PostImage


class UserSerializer(serializers.ModelSerializer):
    """
    Returns user data for authentication, or when other serializers make request, i. e. for comments or posts.
    """
    is_followed = serializers.SerializerMethodField('get_is_followed')

    class Meta:
        model = User

    def get_is_followed(self, instance):
        cur_user_id = self.context['user_id']
        if cur_user_id is not None:
            cur_user = User.objects.get(pk=cur_user_id)
            if cur_user.followers.filter(followed_user=instance).exists():
                return True
            else:
                return False
        else:
            return False

    def to_representation(self, instance):
        return {
            'avatar': self.context['request'].build_absolute_uri(instance.profile.avatar_url),
            'id': instance.id,
            'is_followed': self.get_is_followed(instance),
            'username': instance.username,
        }


class CommentSerializer(serializers.ModelSerializer):
    """ For PostSerializer. """
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('author', 'body', 'id')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']

    def to_representation(self, instance):
        return self.context['request'].build_absolute_uri(instance.image.url)


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField('get_is_liked')
    owner = UserSerializer(read_only=True)

    def get_is_liked(self, instance):
        if instance.likes.filter(id=self.context['user_id']).exists():
            return True
        else:
            return False

    class Meta:
        model = Post
        fields = ('caption', 'comments', 'id', 'images', 'is_liked', 'owner', 'total_likes')



# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = []
# 
#     def to_representation(self, instance):
#         return {
#             'avatar': self.context['request'].build_absolute_uri(instance.avatar_url),
#             'bio': instance.bio,
#         }


# class UserSerializer(serializers.ModelSerializer):
#     is_followed = serializers.SerializerMethodField('get_is_followed')
#     profile = ProfileSerializer(read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'is_followed', 'username', 'profile')
#
#     def get_is_followed(self, user):
#         auth_user_id = self.context['user_id']
#         auth_user = User.objects.get(pk=auth_user_id)
#         if auth_user.followers.filter(followed_user=user).exists():
#             return True
#         else:
#             return False



# class CommentSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#
#     class Meta:
#         model = Comment
#         fields = '__all__'




# class PostSerializer(serializers.ModelSerializer):
#     is_liked = serializers.SerializerMethodField('get_is_liked')
#     images = ImageSerializer(many=True)
#     comments = CommentSerializer(read_only=True, many=True)
#     owner = UserSerializer(read_only=True)
#
#     def get_is_liked(self, post):
#         if post.likes.filter(id=self.context['user_id']).exists():
#             return True
#         else:
#             return False
#
#     class Meta:
#         model = Post
#         fields = ['caption', 'comments', 'id', 'is_liked', 'images', 'owner', 'published_at', 'total_likes']
