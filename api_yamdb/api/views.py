from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import Review, Title
from api.serializers import (TitleSerializer, ReviewSerializer,
                             CommentSerializer)

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
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


class CommentViewSet(viewsets.ModelViewSet):
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
