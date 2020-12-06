from django.db import models
from django.utils import timezone
import datetime
import urllib.request
import urllib.parse
import json


class Library(models.Model):
    title = models.CharField(default="My Library", max_length=50)

    def __str__(self):
        return f"{self.title}"


class Book(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE, related_name="libraries"
    )
    title = models.CharField(max_length=100)
    author = models.CharField(default="Unknown Author", max_length=70)
    read_date = models.DateTimeField("book read date", default=timezone.now)

    def __str__(self):
        return f"{self.title}, {self.author}, {self.library.title}"

    def write_book(self, format="markdown"):
        if self.title is None or len(self.clippings.all()) == 0:
            print("Not writting because name is None.")
            return False

        with open(f"books/{self.title}.md", "w+") as file:
            file.write(f"# {self.title}")
            file.write("\n")
            for h in self.clippings.all():
                clean_text = h.content.replace("\n", " ")
                file.write(f"- {clean_text}")
                file.write("\n")

            file.close()

    def google_book(self):

        base_api_link = "https://www.googleapis.com/books/v1/volumes?q="

        with urllib.request.urlopen(
            base_api_link
            + urllib.parse.quote(self.title)
            + " "
            + urllib.parse.quote(self.author)
        ) as f:
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


class Clip(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="clippings")
    content = models.CharField(max_length=5000)
    book_location = models.IntegerField(default=0)
    date_read = models.DateTimeField(default=datetime.datetime(1900, 1, 1))

    def __str__(self):
        return f"{self.book.title}, {self.content}, {self.book_location}"
