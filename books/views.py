from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BookSerializer
from .models import Book
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema


class BookCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=BookSerializer)
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=BookSerializer)
    def put(self, request, pk):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.permission_classes = [IsAdminUser]
        self.check_permissions(request)
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookByGenreAPIView(APIView):
    def get(self, request, genre_id):
        books = Book.objects.filter(genres__id=genre_id)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
