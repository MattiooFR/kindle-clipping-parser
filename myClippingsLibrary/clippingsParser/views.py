from django.http import HttpResponse
from django.template import loader

from .models import Book


def index(request):
    return HttpResponse("Hello, world. You're at the Clippings index.")


def library(request, library):
    books = Book.objects.filter(library__title=library)

    template = loader.get_template('clippingsParser/library.html')
    context = {
        'books': books,
        'library': library
    }
    return HttpResponse(template.render(context, request))


def book(request, book_id):
    book = Book.objects.get(pk=book_id)

    template = loader.get_template('clippingsParser/book.html')
    context = {
        'title': book.title,
        'author': book.author,
        'library_title': book.library.title,
        'read_date': book.read_date
    }
    return HttpResponse(template.render(context, request))
