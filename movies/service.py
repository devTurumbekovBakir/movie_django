from django_filters import rest_framework
from movies.models import Movie


def get_client_ip(request):
    """"Получение IP пользователя"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(rest_framework.BaseInFilter, rest_framework.CharFilter):
    ...


class MovieFilter(rest_framework.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    year = rest_framework.RangeFilter()  # диапазон

    class Meta:
        model = Movie
        fields = ('genres', 'year',)
