from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import (
    ModelViewSet,
    # ReadOnlyModelViewSet,
    # GenericViewSet
)
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


# from .mixins import ModelMixinSet
from .permissions import IsAdminOrReadOnly, UsersPermission, AdminOnlyPermissions
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    UserSerializer,
    SignUpSerializer,
    AdminSerializer,
    GetTokenSerializer
)
from reviews.models import Category, CustomUser, Genre, Title



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
    http_method_names= ['get', 'post', 'delete', 'patch']
    serializer_class = AdminSerializer 
    queryset = CustomUser.objects.all()
    permission_classes = (AdminOnlyPermissions, )
    # pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, )
    search_fields = ('username',)
    lookup_field= 'username'
    
    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes = (IsAuthenticated, ),
        serializer_class = UserSerializer,
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
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            try:
                username = data['username']
                email = data['email']
                user, create = CustomUser.objects.get_or_create(username=username, email=email)
            except ValueError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
        user =  get_object_or_404(CustomUser,username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user.save()
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)}, status=status.HTTP_201_CREATED)
        # raise  ValidationError(f'Значение {username} или {confirmation_code} не верно. Проверьте данные или пройдите регистрацию заново')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

