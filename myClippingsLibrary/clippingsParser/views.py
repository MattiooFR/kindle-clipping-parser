from django.shortcuts import render
from .models import Book, Library


def index(request):
    librarys = Library.objects.all()

    context = {
        'librarys': librarys
    }
    return render(request, 'clippingsParser/index.html', context)


def library(request, library):
    books = Book.objects.filter(library__title=library)

    context = {
        'books': books,
        'library': library
    }
    return render(request, 'clippingsParser/library.html', context)


def book(request, book_id):
    book = Book.objects.get(pk=book_id)

    context = {
        'title': book.title,
        'author': book.author,
        'library_title': book.library.title,
        'read_date': book.read_date
    }
    return render(request, 'clippingsParser/book.html', context)
