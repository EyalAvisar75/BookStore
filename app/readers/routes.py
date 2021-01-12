from random import randint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import Reader, Book
from app.readers.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from app.books.forms import BookForm
from app.utils import send_reset_email


readers = Blueprint('readers', __name__)


@readers.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit() and form.validate_name(form.name) \
            and form.validate_email(form.email):
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
        return redirect(url_for('readers.login'))
    flash(f'registration failure {form.name.data}', 'danger')
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
    if current_user.role != 'admin':
        form = UpdateAccountForm()
        if form.validate_on_submit():
            form.validate_name(form.name)
            form.validate_email(form.email)
            current_user.name = form.name.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Reader account has been updated', 'success')
        else:
            form.name.data = current_user.name
            form.email.data = current_user.email
        # return render_template('account.html', title='Account', form=form)

    else:
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

@readers.route('/reset_password', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        reader = Reader.query.filter_by(email=form.email.data).first()
        send_reset_email(reader)
        flash('An email has been sent with reset instructions', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@readers.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    reader = Reader.verify_reset_token(token)

    if reader == None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit() and form.validate_name(form.name) \
            and form.validate_email(form.email):
        hashed_password = \
            bcrypt.generate_password_hash(form.password.data)\
                .decode('utf-8')
        reader.password = hashed_password
        db.session.commit()
        flash('Password has been updated successfully', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

