from django_filters import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug',)
    genre = CharFilter(field_name='genre__slug',)
    name = CharFilter(field_name='name',)
    year = NumberFilter(field_name='year',)

    class Meta:
        model = Title
        fields = '__all__'
