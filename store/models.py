from django.db import models
from django.contrib.auth.models import User

from method.models import Genre


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre)
