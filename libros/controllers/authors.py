from flask import render_template, request, redirect
from __init__ import app
from models.author import Author
from models.book import Book

@app.route('/')
def index():
    return redirect('/authors')

@app.route("/authors", methods=["GET"])
def get_authors():
    # llamar al método de clase get all para obtener todos los amigos
    authors = Author.get_all_author()
    
    return render_template("authors.html", authors = authors)


@app.route('/authors', methods=["POST"])
def post_newauthors():
    data = {
        "name": request.form["name"]        
    }
    
    author_id =  Author.newauthor(data)
    
    return redirect('/authors')

@app.route('/authors/<int:id>', methods=["GET"])
def show_author(id):
    data = {
        "id": id
    }
    author=Author.get_by_id(data)
    unfavorited_books=Book.unfavorited_books(data)
    return render_template('show_author.html',author=author,unfavorited_books=unfavorited_books)

@app.route('/join/book',methods=['POST'])
def join_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.add_favorite(data)
    return redirect(f"/authors/{request.form['author_id']}")
