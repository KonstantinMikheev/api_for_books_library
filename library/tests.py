from datetime import datetime
from django.utils.timezone import now

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Book, Author, Genre, Rental
from users.models import User


class AuthorTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.staff_user = User.objects.create(email='library@library.com', is_staff=True)
        self.usual_user = User.objects.create(email='user@user.com')
        self.author = Author.objects.create(name='Author1', country='Country1')

    def test_create_author(self):
        """Тест создания автора"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:authors-list')
        data = {'name': 'Author2', 'country': 'Country2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)

    def test_create_author_double(self):
        """Тест создания автора повторно"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:authors-list')
        data = {'name': 'Author1', 'country': 'Country1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_author_usual_user(self):
        """Тест создания автора у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:authors-list')
        data = {'name': 'Author2', 'country': 'Country2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_author(self):
        """Тест изменения автора"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:authors-detail', kwargs={'pk': self.author.pk})
        data = {'name': 'Author2', 'country': 'Country2'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.get(pk=self.author.pk).name, 'Author2')

    def test_update_author_usual_user(self):
        """Тест изменения автора у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:authors-detail', kwargs={'pk': self.author.pk})
        data = {'name': 'Author2', 'country': 'Country2'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_author(self):
        """Тест получения автора"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:authors-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.author.name)
        self.assertEqual(response.data['country'], self.author.country)

    def test_retrieve_author_usual_user(self):
        """Тест получения автора у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:authors-detail', kwargs={'pk': self.author.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_author(self):
        """Тест удаления автора"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:authors-detail', kwargs={'pk': self.author.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Author.objects.count(), 0)

    def test_delete_author_usual_user(self):
        """Тест удаления автора у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:authors-detail', kwargs={'pk': self.author.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_authors(self):
        """Тест получения списка авторов"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:authors-list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None,
                  'results': [{'id': 7, 'name': 'Author1', 'biography': None, 'country': 'Country1', 'photo': None}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_list_authors_usual_user(self):
        """Тест получения списка авторов у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:authors-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GenreTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.staff_user = User.objects.create(email='library@library.com', is_staff=True)
        self.usual_user = User.objects.create(email='user@user.com')
        self.genre = Genre.objects.create(title='Genre1')

    def test_create_genre(self):
        """Тест создания жанра"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:genres-list')
        data = {'title': 'Genre2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 2)

    def test_create_genre_usual_user(self):
        """Тест создания жанра у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:genres-list')
        data = {'title': 'Genre2'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_genre_double(self):
        """Тест создания жанра повторно"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:genres-list')
        data = {'title': 'Genre1'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_genre_usual_user(self):
        """Тест изменения жанра у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:genres-detail', kwargs={'pk': self.genre.pk})
        data = {'title': 'Genre2'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_genre(self):
        """Тест изменения жанра"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:genres-detail', kwargs={'pk': self.genre.pk})
        data = {'title': 'Genre2'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.get(pk=self.genre.pk).title, 'Genre2')

    def test_retrieve_genre(self):
        """Тест получения жанра"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:genres-detail', kwargs={'pk': self.genre.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.genre.title)

    def test_retrieve_genre_usual_user(self):
        """Тест получения жанра у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:genres-detail', kwargs={'pk': self.genre.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_genre(self):
        """Тест удаления жанра"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:genres-detail', kwargs={'pk': self.genre.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)

    def test_delete_genre_usual_user(self):
        """Тест удаления жанра у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:genres-detail', kwargs={'pk': self.genre.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_genres(self):
        """Тест получения списка жанров"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:genres-list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None,
                  'results': [{'id': 14, 'title': 'Genre1'}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_list_genres_usual_user(self):
        """Тест получения списка жанров у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:genres-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BookTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.staff_user = User.objects.create(email='library@library.com', is_staff=True, is_superuser=True)
        self.usual_user = User.objects.create(email='user@user.com')
        author1 = Author.objects.create(name='Author1', country='Country1')
        self.genre = Genre.objects.create(title='Genre1')
        self.book = Book.objects.create(title='Book1', genre=self.genre)
        self.book.authors.add(author1)
        self.book.save()

    def test_create_book(self):
        """Тест создания книги"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:books-list')
        author2 = Author.objects.create(name='Author2', country='Country2')
        data = {'title': 'Book2', 'genre': self.genre.pk, 'authors': [author2.pk]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_usual_user(self):
        """Тест создания книги у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:books-list')
        author2 = Author.objects.create(name='Author2', country='Country2')
        data = {'title': 'Book2', 'genre': self.genre.pk, 'authors': [author2.pk]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_usual_user(self):
        """Тест изменения книги у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:books-detail', kwargs={'pk': self.book.pk})
        data = {'title': 'Book2'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book(self):
        """Тест получения книги"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:books-detail', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_delete_book(self):
        """Тест удаления книги"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:books-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_usual_user(self):
        """"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:books-detail', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_book(self):
        """Тест получения списка книг"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:books-list')
        response = self.client.get(url)
        data = response.json()
        result = {'count': 1, 'next': None, 'previous': None,
                  'results': [{'pk': 6, 'title': 'Book1', 'genre': 5, 'authors': [19], 'year_of_publication': None}]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    # def test_update_book(self):
    #     """Тест изменения книги"""
    #     self.client.force_authenticate(user=self.staff_user)
    #     url = reverse('library:books-detail', kwargs={'pk': self.book.pk})
    #     data = {'title': 'Book2'}
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Book.objects.get(pk=self.book.pk).title, 'Book2')


class RentalTestCase(APITestCase):
    def setUp(self):
        """Подготовка данных перед тестом"""
        self.staff_user = User.objects.create(email='library@library.com', is_staff=True)
        self.usual_user = User.objects.create(email='user@user.com')
        author1 = Author.objects.create(name='Author1', country='Country1')
        self.genre = Genre.objects.create(title='Genre1')
        self.book = Book.objects.create(title='Book1', genre=self.genre)
        self.book.authors.add(author1)
        self.book.save()

    def test_create_rent_book(self):
        """Тест создания аренды книги"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:rent-list')
        data = {'book': self.book.pk, 'reader': self.usual_user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 1)

    def test_create_rent_book_usual_user(self):
        """Тест создания аренды книги у обычного пользователя"""
        self.client.force_authenticate(user=self.usual_user)
        url = reverse('library:rent-list')
        data = {'book': self.book.pk, 'reader': self.usual_user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rental.objects.count(), 1)

    def test_create_rent_book_invalid_data(self):
        """Тест создания аренды книги с невалидными данными"""
        self.client.force_authenticate(user=self.staff_user)
        url = reverse('library:rent-list')
        data = {'book': 'invalid_book_id', 'reader': self.usual_user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Rental.objects.count(), 0)

    # def test_update_rent_book(self):
    #     """Тест изменения информации об аренде книги"""
    #     self.client.force_authenticate(user=self.staff_user)
    #     rental = Rental.objects.create(book=self.book, reader=self.usual_user)
    #     url = reverse('library:rent-detail', kwargs={'pk': rental.pk})
    #     data = {'is_returned': True}
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Rental.objects.get(pk=rental.pk).is_returned, True)

    # def test_retrieve_rent_book(self):
    #     """Тест получения информации об аренде книги"""
    #     self.client.force_authenticate(user=self.staff_user)
    #     rental = Rental.objects.create(book=self.book, reader=self.usual_user)
    #     url = reverse('library:rent-detail', kwargs={'pk': rental.pk})
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     # self.assertEqual(response.data['book']['title'], self.book.title)

    def test_delete_rent_book(self):
        """Тест удаления аренды книги"""
        self.client.force_authenticate(user=self.staff_user)
        rental = Rental.objects.create(book=self.book, reader=self.usual_user)
        url = reverse('library:rent-detail', kwargs={'pk': rental.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Rental.objects.count(), 0)

    # def test_list_rent_book(self):
    #     """Тест получения списка аренд книг"""
    #     self.client.force_authenticate(user=self.staff_user)
    #     rental1 = Rental.objects.create(book=self.book, reader=self.usual_user, rental_date=now())
    #     url = reverse('library:rent-list')
    #     response = self.client.get(url)
    #     data = response.json()
    #     print("Hello")
    #     print(response.json())
    #     result = {'count': 1, 'next': None, 'previous': None, 'results': [
    #         {'pk': 4, 'reader': 68, 'book': 13, 'rental_date': datetime.now(), 'is_returned': False,
    #          'deadline': None, 'return_date': None}]}
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)

