import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from posts.models import Post, Comment, Group, Follow, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username', read_only=True
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'text',
            'pub_date', 'image', 'group'
        )
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'text',
            'created', 'post'
        )
        read_only_fields = ('author', 'post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 'title', 'slug', 'description'
        )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    following = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    def create(self, validated_data):
        user = self.context.get('request').user
        try:
            following = User.objects.get(
                username=self.context.get('request').data.get('following')
            )
        except User.DoesNotExist:
            raise ValidationError('Такого пользователя нет')
        queryset = (
            self.context.get('view').get_queryset().filter(following=following)
        )
        if following == user or queryset.exists():
            raise ValidationError('Ошибка запроса на подписку')
        validated_data['user'] = user
        validated_data['following'] = following
        return super().create(validated_data)

    class Meta:
        model = Follow
        fields = ('user', 'following')
