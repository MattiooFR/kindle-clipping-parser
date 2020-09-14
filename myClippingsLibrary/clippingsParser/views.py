from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import Http404
from .models import Book, Library


def index(request):
    librarys = Library.objects.all()

    librarys = list(Library.objects.all())
    if not librarys:
        raise Http404("No Library matches the given query.")

    context = {
        'librarys': librarys
    }
    return render(request, 'clippingsParser/index.html', context)


def library(request, library):
    books = get_list_or_404(Book, library__title=library)

    context = {
        'books': books,
        'library': library
    }
    return render(request, 'clippingsParser/library.html', context)


def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    context = {
        'title': book.title,
        'author': book.author,
        'library_title': book.library.title,
        'read_date': book.read_date
    }
    return render(request, 'clippingsParser/book.html', context)
