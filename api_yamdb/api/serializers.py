
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
# from reviews.models import CustomUser
from django.core.exceptions import ValidationError
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    SlugRelatedField,
)

from reviews.models import Category, CustomUser, Genre, Title


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
            'name',
            'year',
            'description',
            'genre',
            'category'
        )
        model = Title


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email','role', 'bio', 'first_name', 'Last_name', )
        model = CustomUser
        read_only_fields = ('role',)
        validators = [
                UniqueTogetherValidator(
                   queryset=CustomUser.objects.all(),
                   fields=('username', 'email'))
            ]


class SignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return CustomUser.objects.get_or_create(**validated_data)

    def validated(self, data):
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
                f'Указанные данные уже есть в базе и '
                f'принадлежат другому пользователю'
            )
        return data

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ('username', 'email',)
        model = CustomUser
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email'))
        ]


class GetTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True, max_length=255)

    class Meta:
        fields = ('username', 'email', 'token', )
        model = CustomUser


class AdminSerialiser(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'first_name',
            'last_name',
            'role',
            'bio',
            'is_staff'
        )
        model = CustomUser

