from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterAPI, GetToken
app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users' )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', GetToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', RegisterAPI.as_view(), name='signup')
    
]