from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from reviews.models import CustomUser
from .serializers import UserSerializer, SignUpSerializer, AdminSerialiser, GetTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .permissions import UsersPermission, AdminOnlyPermissions

class UserViewSet(viewsets.ModelViewSet):
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
    
# class AdminViewSet(viewsets.ModelViewSet):
#     serializer_class = AdminSerialiser
#     queryset = CustomUser.objects.all()
#     permission_classes = [AdminOnlyPermissions, ]

# class ModeratorViewSet(viewsets.ModelViewSet):
#     serializer_class = ModeratorSerializer
#     queryset = CustomUser.objects.all()
   

    
    

