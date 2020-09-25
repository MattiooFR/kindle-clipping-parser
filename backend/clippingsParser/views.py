from django.shortcuts import get_list_or_404
from .models import Book, Library, Clip
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'clippingsParser/index.html'
    context_object_name = 'librarys'

    def get_queryset(self):
        return list(Library.objects.all())


class LibraryView(generic.ListView):
    model = Library
    template_name = 'clippingsParser/library.html'
    context_object_name = 'books'

    def get_queryset(self):
        return get_list_or_404(Book, library__title=self.kwargs['library'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['library'] = self.kwargs['library']
        return context


class BookView(generic.DetailView):
    model = Book
    template_name = 'clippingsParser/book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['clippings'] = context['book'].clippings.all()
        return context
