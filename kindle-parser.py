import re

strings = []

with open('My Clippings.txt', 'r', encoding='utf8') as reader:
    strings = re.split(r'==========', reader.read())

print(strings)
books = {}
for line in strings:
    book_title = line.strip().split("\n")[0]
    print(book_title)
    book_clippings = "\n".join(line.split("\n")[3:])
    if not books.get(book_title):
        books[book_title] = [book_clippings]
    else:
        books[book_title].append(book_clippings)

print(books.keys())
print(books["Make It Stick (Peter C. Brown)"])
