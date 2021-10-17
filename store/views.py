from django.db.models.aggregates import Avg, Count
from django.db.models.expressions import Case, When
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.mixins import UpdateModelMixin

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializer import BookSerializer, UserBookRelationSerializer


# Create your views here.
def store_page(request):
    return render(request, 'index.html', {'books': Book.objects.all()})

class BookView(ModelViewSet):
    queryset = Book.objects.all().annotate(
        annotated_likes=Count(
            Case(When(userbookrelation__like=True, then=1))),
        rating=Avg('userbookrelation__rate')
    ).select_related('user').prefetch_related('readers').order_by('id')
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ['price']
    search_fields = ['name', 'author_name']
    ordering_filter = ['price', 'author_name']

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

class UserBookRelationView(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book'

    def get_object(self):
        obj, _ = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        return obj


def store_app(request):
    return render(request, 'mainapp.html')

def auth(request):
    return render(request, 'oauth.html')
