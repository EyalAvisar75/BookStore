from random import randint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import Reader, Book
from app.readers.forms import RegistrationForm, LoginForm
from app.books.forms import BookForm


readers = Blueprint('readers', __name__)


@readers.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = \
            bcrypt.generate_password_hash(form.password.data)\
                .decode('utf-8')
        reader = Reader()
        reader.name = form.name.data
        reader.email = form.email.data
        reader.password = hashed_password
        if randint(0,1) == 1:
            reader.role = 'admin'
        db.session.add(reader)
        db.session.commit()
        flash(f'Account created for {form.name.data}', 'success')
        return redirect(url_for('main.index'))
    return render_template('register.html', title='Register', form=form)\



@readers.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        reader = Reader.query.filter_by(email=form.email.data).first()
        if reader and bcrypt.check_password_hash(reader.password,
                                                 form.password.data):
            login_user(reader)
            # next_page = request.args.get('next', 'index')
            flash(f'Welcome {reader.name}', 'success')
            return redirect(url_for('main.index'))
        else:
            flash(f'Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@readers.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@readers.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = BookForm()
    if form.validate_on_submit():
        books = Book.query.filter_by(title=form.title.data).all()
        for book in books:
            if book.author == form.author.data:
                flash('This book is already in the database','danger')
        else:
            book = Book()
            book.title = form.title.data
            book.author = form.author.data
            book.summary = form.summary.data
            db.session.add(book)
            db.session.commit()
            flash(f'Added book {book.title}','success')
            form.title.data = ''
            form.author.data = ''
            form.summary.data = ''
    return render_template('account.html', title='Account', form=form)
