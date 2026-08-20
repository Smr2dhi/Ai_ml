from fastapi import FastAPI

app=FastAPI()
books = [ 
    {"id": 1, "title": "Python Basics", "author": "A. Kumar", "category": "programming"}, 
    {"id": 2, "title": "FastAPI Fundamentals", "author": "S. Rao", "category": "programming"}, 
    {"id": 3, "title": "AI for Everyone", "author": "M. Iyer", "category": "ai"}, 
    {"id": 4, "title": "Machine Learning Intro", "author": "A. Kumar", "category": "ai"}, 
] 

@app.get("/books")
def book():
    return books



@app.get("/books/search")
def search(category="", author:str=""):
    results=[]

    for book in books:
        if book["category"].lower()==category.lower() and book["author"].lower()==author.lower():
            results.append(book)
            return {
                "count":len(results),
                "results":results
            }

        else:
            return {"Not found"}




@app.get("/books/count")
def count():
    return len(books)    


@app.get("/books/{book_id}")
def book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            return book

    return {"message": "Book not found"}