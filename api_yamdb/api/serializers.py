from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review, Title

User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):

    def validate(self, attr):
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        # author = self.context['request'].user
        # if Review.objects.filter(title=title, author=author).exists():
        if Review.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к данному произведению!')
        return attr

    class Meta:
        fields = ('id', 'text', 'score', 'pub_date') 
        model = Review


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'text', 'pub_date') 
        model = Comment
