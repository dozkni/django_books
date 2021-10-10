from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from store.models import Book
from store.serializer import BookSerializer

# Create your views here.
def store_page(request):
    return render(request, 'index.html', {'books': Book.objects.all()})

class BookView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def store_app(request):
    return render(request, 'mainapp.html')
