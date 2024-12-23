from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from library.models import Author, Genre, Book, Rental
from users.serializers import UserSerializer


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class BookSerializer(ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'pk',
            'title',
            'genre',
            'authors',
            'year_of_publication',
        )


class RentalSerializer(ModelSerializer):
    reader = UserSerializer
    book = BookSerializer

    class Meta:
        model = Rental
        fields = (
            'pk',
            'reader',
            'book',
            'rental_date',
            'is_returned',
            'deadline',
            'return_date',
        )

