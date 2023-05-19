from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from .filters import TitleFilter
from .permissions import AdminOnlyPermissions, IsAdminOrReadOnly
from .serializers import (AdminSerializer, CategorySerializer,
                          CommentSerializer, GenreSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          SignUpSerializer, TitleGetSerializer,
                          TitlePostSerializer, UserSerializer)

# from django.core.exceptions import ValidationError


class CategoryViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer


class UserViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']
    serializer_class = AdminSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AdminOnlyPermissions, )
    # pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated, ),
        serializer_class=UserSerializer,
        url_path='me')
    def update_profile(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            user = get_object_or_404(CustomUser, pk=request.user.id)
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

    # def get_serializer_class(self):
    #     if self.request.user.is_admin:
    #         return AdminSerializer
    #     return UserSerializer


class RegisterAPI(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        print(111)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            if data['username'] == 'me':
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                username = data['username']
                email = data['email']
                user, create = CustomUser.objects.get_or_create(
                    username=username,
                    email=email
                )
            except ValueError:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject=self.request.user,
                message=(f'Код подтверждения {confirmation_code}'),
                from_email='admin@example.com',
                recipient_list=[user.email],
                fail_silently=False
            )
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        print(data)
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(CustomUser, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user.save()
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_201_CREATED
        )

        # raise  ValidationError(f'Значение {username} или {confirmation_code}
        # не верно. Проверьте данные или пройдите регистрацию заново')
        # return Response(serializer.errors,
        # status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        # serializer.save(author=self.request.user,
        #                title=title)
        serializer.save(title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Review, pk=title_id)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        title = self.get_title()
        # serializer.save(author=self.request.user,
        #                title=title)
        serializer.save(review=review, title=title)
