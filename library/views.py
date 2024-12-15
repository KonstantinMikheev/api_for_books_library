from django.utils.timezone import now
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from library.models import Book, Author, Genre, Rental
from library.paginators import Paginator
from library.serializers import BookSerializer, AuthorSerializer, GenreSerializer, RentalSerializer
from users.permissions import IsLibrarian


class BookViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Book."""

    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('title', 'authors', 'genre', 'description',)
    ordering_fields = ('title', 'genre', 'is_available',)
    filterset_fields = ('title', 'genre', 'is_available',)

    def get_permissions(self):
        """Возвращает список разрешений в зависимости от типа пользователя."""
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = (IsAdminUser | IsLibrarian)
        elif self.action in ['retrieve', 'list',]:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

class AuthorViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Author."""

    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = Paginator
    permission_classes = [IsAdminUser | IsLibrarian]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'country']
    ordering_fields = ['name', 'country']


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделью Genre."""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = Paginator
    permission_classes = [IsAdminUser | IsLibrarian]


class RentalViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения списка арендованных книг."""
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    pagination_class = Paginator


    def get_permissions(self):
        """Возвращает список разрешений в зависимости от типа пользователя."""
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = (IsAdminUser | IsLibrarian)
        elif self.action in ['retrieve', 'list', ]:
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """Делает проверку наличия свободных книг."""
        serializer.save(rental_date=now())
        book = get_object_or_404(Book, pk=serializer.validated_data['book'])
        if book.is_available:
            book.is_available = False
            book.deadline = now() + timedelta(days=30)
            book.save()
        else:
            raise ValidationError('Книга уже на руках.')

    def perform_update(self, serializer):
        """Делает проверку возвращения книги."""
        rental = get_object_or_404(Rental, pk=serializer.instance.pk)
        book = rental.book
        book.is_available = True
        book.save()
        serializer.save(return_date=now())

    def perform_destroy(self, instance):
        """Делает проверку возвращения книги при удалении."""
        rental = get_object_or_404(Rental, pk=instance.pk)
        book = rental.book
        book.is_available = True
        book.save()
        instance.delete()

    def list(self, request, *args, **kwargs):
        if IsLibrarian().has_permission(self.request, self):
            return Rental.objects.all()
        else:
            return Rental.objects.filter(user=self.request.user)
