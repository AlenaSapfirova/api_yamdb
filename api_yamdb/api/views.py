from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import (
    ModelViewSet,
    # ReadOnlyModelViewSet,
    # GenericViewSet
)
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.decorators import action

# from .mixins import ModelMixinSet
from .permissions import IsAdminOrReadOnly, UsersPermission, AdminOnlyPermissions
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    UserSerializer,
    SignUpSerializer,
    AdminSerialiser,
    GetTokenSerializer
)
from reviews.models import Category, CustomUser, Genre, Title


# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework import permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from django.core.mail import send_mail
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
# from rest_framework.decorators import action


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(ModelViewSet):
    # queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    # Заменить queryset после появления моделей R&C
    queryset = Title.objects.annotate(rating=Avg(0))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleGetSerializer
        return TitlePostSerializer

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [UsersPermission,  AdminOnlyPermissions]
    lookup_field = 'username'
    
    @action(methods=['patch'], detail=False, url_path='me')
    def register_user(self, request):
        if request.user.is_admin:
            serializer = AdminSerialiser(request.user, request.data, partial=True)
        else:
            serializer == UserSerializer(request.user, request.data, partial=True)
        return Response(serializer.data)


class RegisterAPI(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        serializer = SignUpSerializer
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        # confirmation_code = default_token_generator.make_token(user)
        try:
            user, created= CustomUser.objects.get_or_create(**serializer.validated_data)
        except Exception as error:
            return Response((f'Ошибка {error}'), status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = default_token_generator.make_token(user)
        user.save()
        send_mail(
            subject = self.request.user,
            message=(f'Код подтверждения {confirmation_code}'),
            from_email = 'admin@example.com',
            recipient_list = [email],
            fail_silently = False
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED) 
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
class GetToken(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = GetTokenSerializer
        if serializer.is_valid:
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            user = CustomUser.objects.get(username=username, confirmation_code=confirmation_code)
            access = RefreshToken.for_user(user).access_token
            return Response({'token': str(access) }, status=status.HTTP_201_CREATED)
        # raise  ValidationError(f'Значение {username} или {confirmation_code} не верно. Проверьте данные или пройдите регистрацию заново')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

