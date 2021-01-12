from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, current_user
from app import db
from app.books.forms import BookEditForm
from app.models import Book

books = Blueprint('books', __name__)


@books.route('/<book_id>/edit_book', methods=['POST', 'GET'])
@login_required
def edit_book(book_id):
    form = BookEditForm()
    book = Book.query.get(book_id)

    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.summary = form.summary.data
        book.price = form.price.data
        db.session.commit()
        flash('Updated book', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.summary.data = book.summary
        form.price.data = book.price

    return render_template('edit_book.html', form=form)


@books.route('/<book_id>', methods=['POST', 'GET'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Deleted book', 'success')
    return redirect(url_for('main.index'))


@books.route('/find_book', methods=['POST'])
def find_book():
    if request.method == 'POST':
        book_name = request.form['book_search']
    book = Book.query.filter_by(title=book_name).first()

    if book is None:
        flash(f'Did not find {book_name}')
        return redirect(url_for('main.index'))
    return render_template('find_book.html', book=book, title="Book Search")


@books.route('/<book_id>/add', methods=['POST', 'GET'])
@login_required
def add_book(book_id):
    book = Book.query.get(book_id)
    current_user.books.append(book)
    db.session.commit()
    flash('Added book', 'success')
    return redirect(url_for('main.index'))


@books.route('/<book_id>/unload', methods=['POST', 'GET'])
@login_required
def unload_book(book_id):
    book = Book.query.get(book_id)
    if book in current_user.books:
        current_user.books.remove(book)
        db.session.commit()
        flash('Unloaded book', 'success')
    else:
        flash('Book not on cart', 'success')
    return redirect(url_for('main.index'))