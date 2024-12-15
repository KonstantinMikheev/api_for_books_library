from django.db import models
from django.db.models import ForeignKey

from config import settings

NULLABLE = {"blank": True, "null": True}


class Author(models.Model):
    """Модель создания автора"""
    name = models.CharField(max_length=300, verbose_name='автор', unique=True)
    biography = models.TextField(verbose_name='биография автора', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='из страны', **NULLABLE)
    photo = models.ImageField(upload_to='library/authors', verbose_name='Фото автора', **NULLABLE)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Genre(models.Model):
    """Модель создания жанра"""

    title = models.CharField(max_length=250, verbose_name='название жанра', help_text='укажите жанр', unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.title


class Book(models.Model):
    """Модель создания книги"""

    title = models.CharField(max_length=250, verbose_name='название книги', help_text='Введите название книги')
    description = models.TextField(verbose_name='описание книги', help_text='Введите описание книги', **NULLABLE)
    authors = models.ManyToManyField(Author, help_text='авторы')
    year_of_publication = models.CharField(max_length=10, verbose_name='год издания', **NULLABLE)
    genre = ForeignKey(Genre, on_delete=models.SET_NULL, verbose_name='жанр книги', **NULLABLE)
    preview = models.ImageField(upload_to='library/books', verbose_name='Изображение книги', **NULLABLE)
    is_available = models.BooleanField(default=True, verbose_name='доступна к выдаче')


    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ('title', 'genre',)

    def __str__(self):
        return self.title


class Rental(models.Model):
    """Модель создания отметки о выдаче книги"""
    reader = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Читатель", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name="Книга выдана", on_delete=models.CASCADE)
    rental_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    return_date = models.DateTimeField(verbose_name="Дата возврата", **NULLABLE)
    is_returned = models.BooleanField(default=False, verbose_name="Возвращена?")
    deadline = models.DateTimeField(help_text="Срок возврата книги")

    def __str__(self):
        return f"{self.reader} - {self.book}"

    class Meta:
        verbose_name = "Выдача"
        verbose_name_plural = "Выдачи"
        ordering = ('-rental_date',)
