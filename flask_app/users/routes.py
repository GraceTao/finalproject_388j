from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required, login_user, logout_user
import base64
from io import BytesIO
from .. import bcrypt
from werkzeug.utils import secure_filename
from ..forms import RegistrationForm, LoginForm, SearchForm, QuizResultsForm
from ..models import User

users = Blueprint("users", __name__)

""" ************ User Management views ************ """


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('careers.index'))
    
    registration_form = RegistrationForm()
    
    if registration_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registration_form.password.data).decode('utf-8')
        new_user = User(username=registration_form.username.data, 
                        email=registration_form.email.data,
                        password=hashed_password)
        new_user.save()
        return redirect(url_for('users.login'))

    return render_template('register.html', form=registration_form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('careers.index'))

    
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.objects(username=login_form.username.data).first()

        if (user is not None) and (bcrypt.check_password_hash(user.password, login_form.password.data)):
            login_user(user)
            user = User.objects(username=current_user.username).first()
            unique_titles = user.saved_job_titles
            unique_codes = user.saved_job_codes
            zipped_jobs = zip(unique_titles, unique_codes)

            return redirect(url_for('users.account'))
        else:
            flash('Incorrect username or password. Please try again.')
    
    return render_template('login.html', form=login_form)


@users.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()

        return redirect(url_for('careers.index'))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("careers.query_results", query=form.search_query.data))
    
    user = User.objects(username=current_user.username).first()
    unique_titles = user.saved_job_titles
    unique_codes = user.saved_job_codes
    zipped_jobs = zip(unique_titles, unique_codes)

    return render_template('account.html', form=form, zipped_jobs=zipped_jobs)


@users.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    quiz_results_form = QuizResultsForm()
    
    if quiz_results_form.validate_on_submit():
        careers = [quiz_results_form.career1.data,
                   quiz_results_form.career2.data,
                   quiz_results_form.career3.data]
        user = User.objects(username=current_user.username).first()
        user.quiz_results.extend(careers)
        user.save()
        return redirect(url_for('users.account')) 
    return render_template('quiz.html', form=quiz_results_form)


