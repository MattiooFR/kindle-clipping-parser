from django.shortcuts import get_list_or_404
from django.http import HttpResponseRedirect

from .models import Book, Library, Clip
from django.views import generic
from django.shortcuts import render

from .forms import UploadClippingsFileForm
from django.urls import reverse_lazy

import re


def import_clippings(clippings):
    strings = re.split(r"==========", clippings.read().decode("utf-8"))
    library = Library(title="Library")
    library.save()

    for line in strings:
        title = line.strip().split("\n")[0].strip()
        clipping = "".join(line.split("\n")[3:])

        if not Book.objects.filter(title=title, library=library):
            book = Book(library=library, title=title)
            book.save()
        else:
            book = Book.objects.get(title=title, library=library)

        clip = Clip(book=book, content=clipping)
        clip.save()


class IndexView(generic.ListView, generic.edit.FormMixin):
    template_name = "clippingsParser/index.html"
    context_object_name = "librarys"
    form_class = UploadClippingsFileForm
    success_url = reverse_lazy("index")

    def get_queryset(self):
        return list(Library.objects.all())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            import_clippings(request.FILES["file"])
            return HttpResponseRedirect("")
        return render(request, self.template_name, {"form": form})


class LibraryView(generic.ListView):
    model = Library
    template_name = "clippingsParser/library.html"
    context_object_name = "books"

    def get_queryset(self):
        return get_list_or_404(Book, library__title=self.kwargs["library"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["library"] = self.kwargs["library"]
        return context


class BookView(generic.DetailView):
    model = Book
    template_name = "clippingsParser/book.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clippings"] = context["book"].clippings.all()
        return context
