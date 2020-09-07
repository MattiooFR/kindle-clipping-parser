from django.db import models


class Library(models.Model):
    title = models.CharField(default='My Library', max_length=50)


class Book(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(default='Unknown Author', max_length=70)
    read_date = models.DateTimeField('book read date')


class Clip(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.CharField(max_length=5000)
    location = models.IntegerField(default=0)
