from django.db import models
from django.contrib.auth.models import User
from rest_framework.fields import empty

from method.models import Genre


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(User, related_name="my_books", on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    author_name = models.CharField(max_length=255)
    readers = models.ManyToManyField(User, related_name="books", through='UserBookRelation')
    
    def __str__(self):
        return f'ID {self.id}: {self.name}'

class UserBookRelation(models.Model):
    RATE_CHOISE = (
        (1, 'Bad'),
        (2, 'Ok'),
        (3, 'Fine'),
        (4, 'Good'),
        (5, 'Best'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOISE, null=True)

    def __str__(self):
        return f'ID {self.user.username}: {self.book.name}, RATE {self.rate}'