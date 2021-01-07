from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required
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
        db.session.commit()
        flash('Updated book', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = book.title
        form.author.data = book.author
        form.summary.data = book.summary

    return render_template('edit_book.html', form=form)


@books.route('/<book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Deleted book', 'success')
    return redirect(url_for('main.index'))

# <button class="btn btn-danger" data-toggle="modal" data-target="#deleteModal">Delete</button>

# <!-- Modal -->
# <!--<div class="modal fade" id="deleteModal" tabindex="-1" role="dialog" aria-labelledby="deleteModalLabel" aria-hidden="true">-->
# <!--  <div class="modal-dialog" role="document">-->
# <!--    <div class="modal-content">-->
# <!--      <div class="modal-header">-->
# <!--        <h5 class="modal-title" id="deletModalLabel">Delete Book?</h5>-->
# <!--        <button type="button" class="close" data-dismiss="modal" aria-label="Close">-->
# <!--          <span aria-hidden="true">&times;</span>-->
# <!--        </button>-->
# <!--      </div>-->
# <!--      <div class="modal-footer">-->
# <!--        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>-->
# <!--        <form action="{{ url_for('delete_book', books.book_id=number) }}" method="post">-->
# <!--            <input class="btn btn-danger" type="submit" value="Delete">-->
# <!--        </form>-->
# <!--      </div>-->
# <!--    </div>-->
# <!--  </div>-->
# <!--</div>-->
