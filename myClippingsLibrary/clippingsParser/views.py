from django.http import HttpResponse
from django.template import loader

from .models import Book


def index(request):
    return HttpResponse("Hello, world. You're at the Clippings index.")


def library(request, library):
    books = ', '.join([str(b)
                       for b in Book.objects.filter(library__title=library)])
    template = loader.get_template('clippingsParser/library.html')
    context = {
        'books': books,
        'library': library
    }
    return HttpResponse(template.render(context, request))


def book(request, library_title, book_id):
    return HttpResponse("This is the book page for the book id : {}".format(book_id))
