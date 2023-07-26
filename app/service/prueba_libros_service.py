#"""
#FastAPI app called 'Bookipedia' that serves information about books and their authors. A simple example of a
#"many-to-many" relationship *without* extra data.
#"""
#
## <SQLAlchemy code not shown...>
#
## <pydantic code not shown...>
#    
#from fastapi import FastAPI, Depends, APIRouter
#from schema.prueba_libros_schema import BookSchema, AuthorSchema
#from model.prueba_libros import Book, Author
#
#from sqlalchemy.orm import Session, joinedload
#
#from pydantic import List
#
#books_routers =  APIRouter()
#
#def get_db():
#    db = Session(bind=engine)
#    try:
#        yield db
#    finally:
#        db.close()
#
#@books_routers.get("/books/{id}", response_model=BookSchema)
#async def get_book(id: int, db: Session = Depends(get_db)):
#    db_book = db.query(Book).options(joinedload(Book.authors)).\
#        where(Book.id == id).one()
#    return db_book
#
#
#@books_routers.get("/books", response_model=List[BookSchema])
#async def get_books(db: Session = Depends(get_db)):
#    db_books = db.query(Book).options(joinedload(Book.authors)).all()
#    return db_books
#
#
#@books_routers.get("/authors/{id}", response_model=AuthorSchema)
#async def get_author(id: int, db: Session = Depends(get_db)):
#    db_author = db.query(Author).options(joinedload(Author.books)).\
#        where(Author.id == id).one()
#    return db_author
#
#
#@books_routers.get("/authors", response_model=List[AuthorSchema])
#async def get_authors(db: Session = Depends(get_db)):
#    db_authors = db.query(Author).options(joinedload(Author.books)).all()
#    return db_authors
