# from rest_framework.response import Response
# from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions

from .models import Movie, Actor
from .serializers import (MovieListSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer,
                          ActorListSerializer, ActorDetailSerializer)

from rest_framework import generics  # status,

from .service import get_client_ip, MovieFilter

from django.db import models


class MovieListView(generics.ListAPIView):
    """Вывод списка Фильмов"""

    serializer = MovieListSerializer
    filter_backend = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).select_related('category').annotate(
            rating_user=models.Count('ratings',
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод фильма"""

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзва к фильму"""

    serializer_class = ReviewCreateSerializer

    # def post(self, request):
    #     review = ReviewCreateSerializer(data=request.data)
    #     if review.is_valid():
    #         review.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга фильму"""

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

    # def post(self, request):
    #     serializer = CreateRatingSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(ip=get_client_ip(request))
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


class ActorListView(generics.ListAPIView):
    """Вывод списка актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод списка актеров и режиссеров"""

    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer
