from django.contrib.auth.models import User
from django.test.testcases import TestCase
from django.db.models import Count, Case, When


from store.models import Book, UserBookRelation
from store.serializer import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        user_1 = User.objects.create(username='test_username_1')
        user_2 = User.objects.create(username='test_username_2')
        user_3 = User.objects.create(username='test_username_3')

        book_1 = Book.objects.create(name='Test book 1', price=25,
                                    author_name='1')
        book_2 = Book.objects.create(name='b2', price=10,
                                    author_name='1')

        UserBookRelation.objects.create(user=user_1, book=book_1, like=True)                                   
        UserBookRelation.objects.create(user=user_2, book=book_1, like=True)                                   
        UserBookRelation.objects.create(user=user_3, book=book_1, like=True)                                   
        UserBookRelation.objects.create(user=user_1, book=book_2, like=True)                                   
        UserBookRelation.objects.create(user=user_2, book=book_2, like=False)                                   
        UserBookRelation.objects.create(user=user_3, book=book_2, like=True)                                   
        
        books = Book.objects.all().annotate(
            annotated_likes=Count(
                Case(When(userbookrelation__like=True, then=1)))).order_by('id')
        #data = BookSerializer([book_1, book_2], many=True).data
        data = BookSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': '1',
                'likes_count': 3,
                'annotated_likes': 3
            },
            {
                'id': book_2.id,
                'name': 'b2',
                'price': '10.00',
                'author_name': '1',
                'likes_count': 2,
                'annotated_likes': 2
            },
        ]
        
        self.assertEqual(expected_data, data)
