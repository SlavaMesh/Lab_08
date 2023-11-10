from django_filters import FilterSet, DateFromToRangeFilter
from .models import Post


class PostFilter(FilterSet):
    date = DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ('author', 'date')
