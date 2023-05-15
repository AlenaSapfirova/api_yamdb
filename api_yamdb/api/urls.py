from django.urls import include, path
from rest_framework.views import APIView
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import UserViewSet, RegisterAPI, GetToken
app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users' )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/token/', GetToken.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', RegisterAPI.as_view(), name='signup')
    
]
