from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import (
    ModelViewSet,
    # ReadOnlyModelViewSet,
    # GenericViewSet
)

# from .mixins import ModelMixinSet
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
)
from reviews.models import Category, Genre, Title


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
