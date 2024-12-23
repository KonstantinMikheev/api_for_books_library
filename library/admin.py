from django.contrib import admin

from library.models import Book, Author, Genre, Rental
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "User" в административной панели"""

    list_display = (
        'pk',
        'email',
        'first_name',
        'last_name',
        'phone',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Book" в административной панели"""

    list_display = (
        'pk',
        'title',
        'year_of_publication',
        'genre',
    )
    list_filter = (
        'year_of_publication',
        'genre',
    )

    search_fields =(
        'title',
        'authors',
        'year_of_publication',
        'genre',
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Author" в административной панели"""
    list_display = (
        'pk',
        'name',
        'country',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Genre" в административной панели"""
    list_display = (
        'title',
    )


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Booking" в административной панели"""
    list_display = (
        'pk',
        'reader',
        'book',
        'rental_date',
        'is_returned',
        'deadline',
    )
