from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializer import BookSerializer
from rest_framework import status


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.book_1 = Book.objects.create(name='Test book 1', price = 25, author_name='1')
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

     