from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from store.models import Book
from store.serializer import BookSerializer

# Create your views here.
def store_page(request):
    return render(request, 'index.html', {'books': Book.objects.all()})

class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_filter = ['price', 'author_name']

def store_app(request):
    return render(request, 'mainapp.html')
