from django.db import models
from django.utils import timezone


class Library(models.Model):
    title = models.CharField(default='My Library', max_length=50)

    def __str__(self):
        return f"{self.title}"


class Book(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name='libraries')
    title = models.CharField(max_length=100)
    author = models.CharField(default='Unknown Author', max_length=70)
    read_date = models.DateTimeField(
        'book read date', default=timezone.now)

    def __str__(self):
        return f"{self.title}, {self.author}, {self.library.title}"


class Clip(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='clippings')
    content = models.CharField(max_length=5000)
    book_location = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.book.title}, {self.content}, {self.book_location}"
