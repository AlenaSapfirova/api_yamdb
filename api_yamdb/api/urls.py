from django.urls import include, path

from rest_framework import routers

from api.views import TitleViewSet, ReviewViewSet, CommentViewSet

router_v1 = routers.SimpleRouter()
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
