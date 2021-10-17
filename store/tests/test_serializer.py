from django.contrib.auth.models import User
from django.db.models.aggregates import Avg
from django.test.testcases import TestCase
from django.db.models import Count, Case, When


from store.models import Book, UserBookRelation
from store.serializer import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        user_1 = User.objects.create(username='test_username_1',
                                     first_name='Ivan', last_name='Petrov')
        user_2 = User.objects.create(username='test_username_2',
                                     first_name='Egor', last_name='Sidorov')
        user_3 = User.objects.create(username='test_username_3',
                                     first_name='1', last_name='2')

        book_1 = Book.objects.create(name='Test book 1', price=25,
                                     author_name='1', user=user_1)
        book_2 = Book.objects.create(name='b2', price=10,
                                     author_name='1')

        UserBookRelation.objects.create(user=user_1, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user_2, book=book_1, like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user_3, book=book_1, like=True,
                                        rate=4)
        UserBookRelation.objects.create(user=user_1, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user_2, book=book_2, like=False,
                                        rate=4)
        UserBookRelation.objects.create(user=user_3, book=book_2, like=True)

        books = Book.objects.all().annotate(
            annotated_likes=Count(
                Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': '1',
                'annotated_likes': 3,
                'rating': '4.67',
                'owner_name': 'test_username_1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Egor',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'b2',
                'price': '10.00',
                'author_name': '1',
                'annotated_likes': 2,
                'rating': '3.50',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Egor',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': '1',
                        'last_name': '2'
                    }
                ]
            },
        ]
        
        self.assertEqual(expected_data, data)
