from django.shortcuts import get_list_or_404

from .models import Book, Library, Clip
from django.views import generic
from django.shortcuts import render, redirect

from .forms import UploadClippingsFileForm
from django.urls import reverse_lazy

import re
from dateutil.parser import parse as dateparser


import urllib.request
import urllib.parse
import json


def google_book(search):

    base_api_link = "https://www.googleapis.com/books/v1/volumes?q="

    with urllib.request.urlopen(base_api_link + urllib.parse.quote(search)) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text)  # deserializes decoded_text to a Python object
    volume_info = obj["items"][0]
    authors = volume_info["volumeInfo"].get("authors", [])

    book = {}

    book["title"] = volume_info["volumeInfo"].get("title")
    book["summary"] = volume_info.get("searchInfo", {}).get(
        "textSnippet", "No summary found"
    )
    book["authors"] = ", ".join(authors)
    book["page_number"] = volume_info["volumeInfo"].get("pageCount")
    book["language"] = volume_info["volumeInfo"].get("language")

    return book


def import_clippings(library_title, clippings):
    """Parse the clippings file text and save the books and clips in the database

    Args:
        library_title (string): The name of the library to save datas in
        clippings (text file): The text file that contains all the clippings
    """

    # Parse the file text by clippings
    highlight_separator = "=========="
    strings = re.split(highlight_separator, clippings.read().decode("utf-8"))
    library = Library(title=library_title)
    library.save()

    # Each line represent a highlighted clip
    for highlight_string in strings:
        # To prevent error when parsing empty clip
        if len(highlight_string) >= 5:
            splitted_string = highlight_string.strip().split("\n")

            # Extract the title
            author_line = splitted_string[0].strip()
            match = re.search(r"\((.*)\)", author_line)
            authors = re.findall(r"\((.*?)\)", author_line)
            clipping = splitted_string[3]

            if match:
                author = authors[-1]
                book_title = author_line[: match.start()]

                book_title = "".join(
                    [c for c in book_title if c.isalpha() or c.isdigit() or c == " "]
                ).rstrip()
            else:
                author = "Unknown"
                book_title = author_line

            # Extract the clip metadata, such as book location and when it was highlighted
            clip_metadata = splitted_string[1].strip()
            book_location = clip_metadata.split(" | ")[0].split(" ")[-1].split("-")[0]
            date_read = dateparser(
                clip_metadata.split(" | ")[1].split("Added on ")[1].strip()
            )

            # Create a book in the database if it doesn't exist
            # or get the book corresponding to the clip

            if not Book.objects.filter(title=book_title, library=library):
                book = Book(
                    library=library,
                    title=book_title,
                    read_date=date_read,
                    author=author,
                )
                book.save()
            else:
                book = Book.objects.get(title=book_title, library=library)

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

    # for book in Book.objects.filter(library=library):
    #     gbook = google_book(book.title)
    #     book.title = gbook["title"]
    #     book.author = gbook["authors"]
    #     book.save()


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
