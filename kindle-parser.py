import re


class Books:

    def __init__(self, title='My Kindle Library', books={}):
        self.books = books

    def addBook(self, book):
        if not self.books.get(book.title):
            self.books[book.title] = book

    def getBook(self, bookTitle):
        return self.books.get(bookTitle)

    def __str__(self):
        return "Books in library : " + ", ".join([key for key in self.books.keys()])[:-2]


class Book:

    def __init__(self, title='Unknown Title', clippings=[]):
        self.title = title
        self.clippings = clippings

    def getClippings(self):
        return self.clippings

    def __str__(self):
        return str(self.getClippings())


Library = Books()

with open('My Clippings.txt', 'r', encoding='utf8') as reader:
    strings = re.split(r'==========', reader.read())

for line in strings:
    book_title = line.strip().split("\n")[0]
    Library.addBook(Book(book_title))

    book_clippings = "\n".join(line.split("\n")[3:])
    print(book_clippings)

    if not Library.getBook(book_title):
        Library.books[book_title].clippings = [book_clippings]
    else:
        Library.books[book_title].clippings.append(book_clippings)


print(Library)
#print(Library.books['The Elon Musk Blog Series: Wait But Why (Urban, Tim)'])
