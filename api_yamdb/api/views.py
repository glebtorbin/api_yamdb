from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewsSerializer,
                             TitleCreateSerializer, TitleListSerializer)
from reviews.models import Category, Genre, Review, Title


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    )
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    pagination_class = LimitOffsetPagination
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return TitleCreateSerializer
        return TitleListSerializer


class GenreViewSet(CreateModelMixin,
                   ListModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateModelMixin,
                      ListModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorAdminModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorAdminModeratorOrReadOnly,
        IsAuthenticatedOrReadOnly
    )
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
