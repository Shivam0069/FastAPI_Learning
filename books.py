from fastapi import FastAPI, Body
from typing import Optional

app = FastAPI()


BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/")
def home_route():
    return {"message": "Hello World"}


# @app.get("/about")
# def about_route():
#     return {"message": "About Page"}


@app.get("/books")
def read_all_books():
    return BOOKS


# When we require whats written in url we use {variable_name}
# casefold() is used to make the string case insensitive
@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book


# we are using query parameter to get the category
@app.get("/books/")
def read_books_by_category_by_query(category: Optional[str] = None):
    books = []
    if category:
        for book in BOOKS:
            if book["category"].casefold() == category.casefold():
                books.append(book)
        return books
    return BOOKS


@app.get("/books/byauthor/")
def read_books_by_author(author: str):
    books = []
    for book in BOOKS:
        if book["author"].casefold() == author.casefold():
            books.append(book)
    return books


@app.get("/books/{author}/")
def read_books_by_author_category(author: str, category: str):
    books = []
    for book in BOOKS:
        if (
            book["author"].casefold() == author.casefold()
            and book["category"].casefold() == category.casefold()
        ):
            books.append(book)
    return books


@app.post("/books/create_book")
def create_book(book=Body()):
    # print(book)
    BOOKS.append(book)
    return {"message": "Book Created", "books": BOOKS}


@app.put("/books/update_book")
def update_book(updated_book=Body()):
    for book in BOOKS:
        if book.get("title").casefold() == updated_book.get("title").casefold():
            book.update(updated_book)
            return {"message": "Book Updated", "books": BOOKS}
    return {"message": "Book not found"}


@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            BOOKS.remove(book)
            break
    return {"message": "Book Deleted", "books": BOOKS}
