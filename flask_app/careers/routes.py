import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from pytest import console_main

from .. import careers_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Profile #, Quiz
from ..utils import current_time

careers = Blueprint("careers", __name__)
""" ************ Helpers ************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image


""" ************ View functions ************ """

@careers.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("careers.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)

@careers.route("/all-careers/<int:start>", methods=["GET"])
def all_careers(start):
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("careers.query_results", query=form.search_query.data))
    
    end = start + 19  # Show 20 careers per page
    path = 'mnm/careers/'
    query = {'sort': "name", 'start': start, 'end': end}
    response = careers_client.call(path, query)

    careers_list = response.get("career", [])
    total = response.get("total", 0)  # Total number of careers

    next_start = start + 20 if end < total else None
    prev_start = start - 20 if start > 1 else None
    print(prev_start)
    
    return render_template(
        "all_careers.html",
        careers=careers_list,
        current_start=start,
        prev_start=prev_start,
        next_start=next_start,
        form=form
    )


@careers.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("careers.query_results", query=form.search_query.data))
    
    results = careers_client.call(f'mnm/search/', {'keyword': query, 'start': 1, 'end': 21})
    
    return render_template("query.html", results=results, form=form)


@careers.route("/career/<code>", methods=["GET", "POST"])
def career_detail(code):
    print(code)
    career = careers_client.call(f'mnm/careers/{code}/report', {})
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("careers.query_results", query=form.search_query.data))
    # form = MovieReviewForm()
    # if form.validate_on_submit():
    #     review = Review(
    #         commenter=current_user._get_current_object(),
    #         content=form.text.data,
    #         date=current_time(),
    #         imdb_id=movie_id,
    #         movie_title=result.title,
    #     )

    #     review.save()

    #     return redirect(request.path)

    # reviews = Review.objects(imdb_id=movie_id)

    return render_template("career_detail.html", career=career, form=form)