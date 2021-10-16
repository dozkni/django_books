from rest_framework.test import APITestCase
from django.urls import reverse
from method.models import Genre
from store.models import Book, UserBookRelation
from store.serializer import BookSerializer
from rest_framework import status
import json
from django.contrib.auth.models import User


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.genre = Genre.objects.create(name='Test genre')
        self.book_1 = Book.objects.create(name='Test book 1', price = 25, author_name='1', user = self.user)
        self.book_2 = Book.objects.create(name='b2', price = 10, author_name='1')
        self.book_3 = Book.objects.create(name='Test book 3', price = 50, author_name='b2 a')

    def test_get(self):
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'price': 25})
        serializer_data = BookSerializer([self.book_1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': 'b2'})
        serializer_data = BookSerializer([self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        countBooks = Book.objects.all().count()
        url = reverse('book-list')
        data = {
            "name": "Python 3",
            "price": 99,
            "author_name": "Mark Sammerfield",
            "genres": [1]
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(countBooks + 1, Book.objects.all().count())
        self.assertEqual(self.user, Book.objects.last().user)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 222,
            "author_name": self.book_1.author_name,
            "genres": []
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.book_1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(222, Book.objects.get(id=self.book_1.id).price)

    def test_update_not_owner(self):
        self.user2 = User.objects.create(username='test_username2')
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            "name": self.book_1.name,
            "price": 222,
            "author_name": self.book_1.author_name,
            "genres": []
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

class BooksRelationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_username')
        self.user2 = User.objects.create(username='test_username2')
        self.genre = Genre.objects.create(name='Test genre')
        self.book_1 = Book.objects.create(name='Test book 1', price = 25, author_name='1', user = self.user)
        self.book_2 = Book.objects.create(name='b2', price = 10, author_name='1')
        self.book_3 = Book.objects.create(name='Test book 3', price = 50, author_name='b2 a')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id,))
        data = {
            "like": True
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.user,
                                                book=self.book_1)
        self.assertTrue(relation.like)

