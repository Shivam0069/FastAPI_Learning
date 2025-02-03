from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(
        description="Id not required while creating a book", default=None
    )
    title: str = Field(
        ...,
        min_length=3,
        error_messages={"min_length": "Title must be at least 3 characters long"},
    )
    author: str = Field(
        ...,
        min_length=3,
        error_messages={"min_length": "Author must be at least 3 characters long"},
    )
    description: str = Field(
        ...,
        min_length=3,
        max_length=100,
        error_messages={
            "min_length": "Description must be at least 3 characters long",
            "max_length": "Description must be at most 100 characters long",
        },
    )
    rating: int = Field(
        ...,
        ge=1,
        le=5,
        error_messages={
            "ge": "Rating must be at least 1",
            "le": "Rating must be at most 5",
        },
    )
    published_date: int = Field(
        ...,
        ge=2022,
        le=2030,
        error_messages={
            "ge": "Published date must be at least 2022",
            "le": "Published date must be at most 2030",
        },
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
def read_book_by_publish_date(publish_date: int = Query(..., ge=2022, le=2030)):
    books = []
    for book in BOOKS:
        if book.published_date == publish_date:
            books.append(book)
    if len(books) > 0:
        return books
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
def read_book_by_rating(rating: int = Query(..., ge=1, le=5)):
    books = []
    for book in BOOKS:
        if book.rating == rating:
            books.append(book)
    if len(books) > 0:
        return books
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@app.post("/create_book")
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_update = False
    for b in range(len(BOOKS)):
        if BOOKS[b].id == book.id:
            BOOKS[b] = book
            book_update = True
            break
    if not book_update:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for book in BOOKS:
        if book.id == book_id:
            BOOKS.remove(book)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Book not found")
