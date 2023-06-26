
from config.mysqlconnection import connectToMySQL
from models import book

class Author:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books  = []
    
    @classmethod
    def get_all_author(cls):
        query = "SELECT * FROM autores;"
        authors = []
        results = connectToMySQL('libros').query_db(query)
        
        for author in results:
            authors.append( cls(author) )
        return authors

    @classmethod
    def newauthor(cls, data ):
        query = "INSERT INTO autores ( name , created_at, updated_at ) VALUES ( %(name)s , NOW() , NOW() );"
        return connectToMySQL('libros').query_db( query, data )        

    @classmethod
    def unfavorited_authors(cls,data):
        query = "SELECT * FROM autores WHERE autores.id NOT IN ( SELECT author_id FROM favoritos WHERE book_id = %(id)s );"
        authors = []
        results = connectToMySQL('libros').query_db(query,data)
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def add_favorite(cls,data):
        query = "INSERT INTO favoritos (author_id,book_id) VALUES (%(author_id)s,%(book_id)s);"
        return connectToMySQL('libros').query_db(query,data);


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM autores LEFT JOIN favoritos ON autores.id = favoritos.author_id LEFT JOIN libros ON libros.id = favoritos.book_id WHERE autores.id = %(id)s;"
        results = connectToMySQL('libros').query_db(query,data)

        # Creates instance of author object from row one
        author = cls(results[0])
        # append all book objects to the instances favorites list.
        for row in results:
            # if there are no favorites
            if row['libros.id'] == None:
                break
            # common column names come back with specific tables attached
            data = {
                "id": row['libros.id'],
                "titulo": row['titulo'],
                "num_paginas": row['num_paginas'],
                "created_at": row['libros.created_at'],
                "updated_at": row['libros.updated_at']
            }
            author.favorite_books.append(book.Book(data))
        return author