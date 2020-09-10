from django.http import HttpResponse
from .models import Book


def index(request):
    return HttpResponse("Hello, world. You're at the Clippings index.")


def library(request, library):
    books = ', '.join([str(b)
                       for b in Book.objects.filter(library__title=library)])
    return HttpResponse("This is the library id : {} with these books {}".format(library, books))


def book(request, library_title, book_id):
    return HttpResponse("This is the book page for the book id : {}".format(book_id))
