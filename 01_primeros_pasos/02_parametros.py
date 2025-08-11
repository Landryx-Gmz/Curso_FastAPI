from fastapi import FastAPI

app = FastAPI()

@app.get("/books/favorite")
async def get_favoritre_book():
    return {"title" : "1984"}

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    return {"book_id": book_id}

