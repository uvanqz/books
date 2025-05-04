from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Book, Genre


class BookAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="password")
        self.admin_user = User.objects.create_user(
            username="admin_user", password="password", is_staff=True
        )
        self.author = Author.objects.create(name="Test Author")
        self.genre = Genre.objects.create(name="Test Genre")

        self.book_data = {
            "title": "Test Book",
            "type": "comic",
            "volume": 2000,
            "year": 2023,
            "description": "Test Description",
            "genres": [self.genre.id],
            "authors": [self.author.id],
        }

        self.book = Book.objects.create(
            title="Test Book",
            type="comic",
            volume="2000",
            year=2023,
            description="Test Description",
            owner=self.user,
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)

        self.book_create_url = reverse("books:book_create")
        self.book_list_url = reverse("books:book_list")
        self.book_detail_url = reverse("books:book_detail", args=[self.book.id])
        self.book_update_url = reverse("books:book_detail", args=[self.book.id])

    def test_create_book_as_admin(self):
        self.client.login(username="admin_user", password="password")
        self.book_data["owner"] = self.user.id
        response = self.client.post(self.book_create_url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.book_data["title"])

    def test_create_book_as_normal_user(self):
        self.client.login(username="test_user", password="password")
        response = self.client.post(self.book_create_url, self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_book_list(self):
        self.client.login(username="test_user", password="password")
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_book_detail(self):
        self.client.login(username="test_user", password="password")
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)

    def test_update_book_as_admin(self):
        updated_data = {
            "title": "Test Book 1",
            "type": "magazine",
            "volume": 2001,
            "year": 2023,
            "description": "Test Description 1",
            "genres": [self.genre.id],
            "authors": [self.author.id],
            "owner": self.user.id,
        }
        self.client.login(username="admin_user", password="password")
        response = self.client.put(
            self.book_update_url, updated_data, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_data["title"])

    def test_update_book_as_normal_user(self):
        updated_data = {
            "title": "Test Book 1",
            "type": "magazine",
            "volume": 2001,
            "year": 2023,
            "description": "Test Description 1",
            "genres": [self.genre.id],
            "authors": [self.author.id],
            "owner": self.user.id,
        }
        self.client.login(username="test_user", password="password")
        self.book_data["owner"] = self.user.id
        response = self.client.put(self.book_update_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_as_admin(self):
        self.client.login(username="admin_user", password="password")
        response = self.client.delete(self.book_update_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_as_normal_user(self):
        self.client.login(username="test_user", password="password")
        response = self.client.delete(self.book_update_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_books_by_genre(self):
        self.client.login(username="test_user", password="password")
        url = reverse("books:books_genre", args=[self.genre.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book.title)

    def test_get_books_by_nonexistent_genre(self):
        self.client.login(username="test_user", password="password")
        url = reverse("books:books_genre", args=[999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
