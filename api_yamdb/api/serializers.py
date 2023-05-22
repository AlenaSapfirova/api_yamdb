from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    SlugRelatedField
)
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from users.models import CustomUser, TYPE_MODELS


class CategorySerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGetSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title


class TitlePostSerializer(ModelSerializer):
    rating = IntegerField(read_only=True, default=0)
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(
            instance=instance.category,
            read_only=True
        ).data
        representation['genre'] = GenreSerializer(
            instance=instance.genre,
            read_only=True,
            many=True
        ).data
        return representation


class UserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    role = serializers.ChoiceField(
        choices=TYPE_MODELS,
        required=False,
        read_only=True
    )

    class Meta:
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )
        model = CustomUser
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email'))
        ]


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    email = serializers.EmailField(required=True, max_length=150)

    def validate(self, data):
        email = data['email']
        username = data['username']
        if (
            CustomUser.objects.filter(email=email).exists()
            and CustomUser.objects.get(email=email).username != username
        ) or (
            CustomUser.objects.filter(username=username).exists()
            and CustomUser.objects.get(username=username).email != email
        ):
            raise ValidationError(
                'Указанные данные уже есть в базе и '
                'принадлежат другому пользователю'
            )
        return data

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Ошибка! Выберете другое имя.')
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    confirmation_code = serializers.CharField(max_length=255)


class AdminSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=TYPE_MODELS, default='user')
    last_name = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)

    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'role',
            'bio',
            'email',
        )
        model = CustomUser
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email'))
        ]


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, attrs):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        author = request.user
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к данному произведению!'
            )
        return attrs

    class Meta:
        author = serializers.SlugRelatedField(
            slug_field='username',
            read_only=True
        )
        fields = ('id', 'text', 'score', 'pub_date', 'author')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = (
            'id',
            'text',
            'author',
            'pub_date'
        )
        model = Comment
