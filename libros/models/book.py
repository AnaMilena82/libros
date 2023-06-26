# importar la función que devolverá una instancia de una conexión
from config.mysqlconnection import connectToMySQL
from models import author
# modelar la clase después de la tabla friend de nuestra base de datos
class Book:
    def __init__( self , data ):
        self.id = data['id']
        self.titulo = data['titulo']
        self.num_paginas = data['num_paginas']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = []
    # ahora usamos métodos de clase para consultar nuestra base de datos
    @classmethod
    def get_all_book(cls):
        query = "SELECT * FROM libros;"
        books = []
        results = connectToMySQL('libros').query_db(query)
        
        for book in results:
            books.append( cls(book) )
        return books

    @classmethod
    def newbook(cls, data ):
        query = "INSERT INTO libros ( titulo , num_paginas, created_at, updated_at ) VALUES ( %(titulo)s ,%(num_paginas)s, NOW() , NOW() );"
        # data es un diccionario que se pasará al método de guardar desde server.py
        return connectToMySQL('libros').query_db( query, data )        

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM libros LEFT JOIN favoritos ON libros.id = favoritos.book_id LEFT JOIN autores ON autores.id = favoritos.author_id WHERE libros.id = %(id)s;"
        results = connectToMySQL('libros').query_db(query,data)

        book = cls(results[0])

        for row in results:
            if row['autores.id'] == None:
                break
            data = {
                "id": row['autores.id'],
                "name": row['name'],
                "created_at": row['autores.created_at'],
                "updated_at": row['autores.updated_at']
            }
            book.authors_who_favorited.append(author.Author(data))
        return book

    @classmethod
    def unfavorited_books(cls,data):
        query = "SELECT * FROM libros WHERE libros.id NOT IN ( SELECT book_id FROM favoritos WHERE author_id = %(id)s );"
        results = connectToMySQL('libros').query_db(query,data)
        books = []
        for row in results:
            books.append(cls(row))
        print(books)
        return books

 