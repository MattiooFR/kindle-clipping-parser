from django.shortcuts import get_list_or_404

from .models import Book, Library, Clip
from django.views import generic
from django.shortcuts import render, redirect

from .forms import UploadClippingsFileForm
from django.urls import reverse_lazy

import re
from dateutil.parser import parse as dateparser


def import_clippings(library_title, clippings):
    """Parse the clippings file text and save the books and clips in the database

    Args:
        library_title (string): The name of the library to save datas in
        clippings (text file): The text file that contains all the clippings
    """

    # Parse the file text by clippings
    strings = re.split(r"==========", clippings.read().decode("utf-8"))
    library = Library(title=library_title)
    library.save()

    # Each line represent a highlighted clip
    for line in strings:
        # To prevent error when parsing empty clip
        if len(line) >= 5:
            line = line.strip()

            # Extract the title
            title = line.split("\n")[0].strip()

            # Extract the highlighted content
            clipping = "".join(line.split("\n")[3:]).strip()

            # Extract the clip metadata, such as book location and when it was highlighted
            clip_metadata = line.split("\n")[1].strip()
            book_location = clip_metadata.split(" | ")[0].split(" ")[-1].split("-")[0]
            date_read = dateparser(
                clip_metadata.split(" | ")[1].split("Added on ")[1].strip()
            )

            # Create a book in the database if it doesn't exist
            # or get the book corresponding to the clip
            if not Book.objects.filter(title=title, library=library):
                book = Book(library=library, title=title, read_date=date_read)
                book.save()
            else:
                book = Book.objects.get(title=title, library=library)

            # There are sometime dupplicate of clippings in the text file because kindle
            # keeps previously edited clippings, this is to keep the latest
            if Clip.objects.filter(
                book=book,
                content__startswith=clipping[: len(clipping) // 3],
                book_location=book_location,
            ).exists():
                clip = Clip.objects.get(
                    book=book,
                    content__startswith=clipping[: len(clipping) // 3],
                    book_location=book_location,
                )
                clip.content = clipping
            else:
                # Save the highlight in the database
                clip = Clip(
                    book=book,
                    content=clipping,
                    book_location=book_location,
                    date_read=date_read,
                )
            clip.save()


class IndexView(generic.ListView, generic.edit.FormMixin):
    template_name = "clippingsParser/index.html"
    context_object_name = "librarys"
    form_class = UploadClippingsFileForm
    success_url = reverse_lazy("clippingsParser:index")

    def get_queryset(self):
        return list(Library.objects.all())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            import_clippings(request.POST["library_title"], request.FILES["file"])
            return redirect(self.success_url)
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
