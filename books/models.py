from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    BOOK_TYPE_CHOICES = [
        ("book", "Книга"),
        ("magazine", "Журнал"),
        ("comic", "Комикс"),
        ("other", "Другое"),
    ]
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=BOOK_TYPE_CHOICES, default="other")
    volume = models.PositiveIntegerField()
    year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
