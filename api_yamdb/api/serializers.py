from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
# from reviews.models import CustomUser

from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    SlugRelatedField,
)

from reviews.models import (
    Category,
    Comment,
    CustomUser,
    Genre,
    Review,
    Title,
    TYPE_MODELS
)


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
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title

        def validate_name(self, value):
            if len(value) > 256:
                raise serializers.ValidationError(
                    'Название произведения не может быть длиннее 256 символов.'
                )
            return value


class UserSerializer(serializers.ModelSerializer):
    last_name = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(required=False)
    # username = serializers.CharField(max_length=150, required=True)
    # # email = serializers.EmailField(required=True)
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


class GetTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(max_length=150,
                                      regex=r'^[\w.@+-]+\Z', required=True)
    # email = serializers.EmailField(required=True, max_length=150)
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

    def validate(self, attr):
        title_id = self.context.get('view').kwargs.get('title_id')
        # title_id = self.context['view'].kwargs.get('title_id')  # такой вариант написания встречал
        title = get_object_or_404(Title, pk=title_id)
        # author = self.context['request'].user
        # if Review.objects.filter(title=title, author=author).exists():
        if Review.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к данному произведению!')
        return attr

    class Meta:
        fields = ('id', 'text', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'pub_date')
        model = Comment
