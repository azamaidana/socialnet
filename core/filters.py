import django_filters
from .models import *

class ShortFilter(django_filters.FilterSet):
    qty_gt = django_filters.NumberFilter(
        field_name='views_qty',
        lookup_expr='gt'
    )
    qty_lt = django_filters.NumberFilter(
        field_name='views_qty',
        lookup_expr='lt'
    )
    class Meta:
        model = Short
        fields = ['user']

class PostFilter(django_filters.FilterSet):
    likes_gt = django_filters.NumberFilter(
        field_name='likes',
        lookup_expr='gt'
    )
    likes_lt = django_filters.NumberFilter(
        field_name='likes',
        lookup_expr='lt'
    )

    class Meta:
        model = Post
        fields = ['creator']