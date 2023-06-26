from flask import render_template, request, redirect, url_for
from __init__ import app
from models.author import Author
from models.book import Book


@app.route("/books", methods=["GET"])
def get_new_books():
    # llamar al método de clase get all para obtener todos los amigos
    books = Book.get_all_book()
    return render_template("new_books.html", books = books)


@app.route('/books', methods=["POST"])
def post_new_books():
    data = {
        "titulo": request.form["titulo"],  
        "num_paginas": request.form["num_paginas"], 
        
    }
    
    book_id = Book.newbook(data)
    
    return redirect(url_for('get_new_books') )

@app.route('/books/<int:id>')
def show_book(id):
    data = {
        "id":id
    }
    book=Book.get_by_id(data)
    unfavorited_authors=Author.unfavorited_authors(data)

    return render_template('show_book.html',book=book,unfavorited_authors=unfavorited_authors)

@app.route('/join/author',methods=['POST'])
def join_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_favorite(data)
    return redirect(f"/books/{request.form['book_id']}")