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

def get_careers(start, end, sort):
    """
    Fetches careers with pagination support.
    
    Args:
        start (int): Starting index of the careers to fetch.
        end (int): Ending index of the careers to fetch.
        sort (str): Sorting parameter (default is 'name').
        
    Returns:
        dict: JSON response with careers and pagination info.
    """
    path = 'mnm/careers/'
    query = {'sort': sort, 'start': start, 'end': end}
    return careers_client.call(path, query)


""" ************ View functions ************ """


@careers.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("careers.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)

@careers.route("/all-careers<int:start>", methods=["GET"])
def all_careers(start):
    # Get 'start' and 'end' query parameters, with defaults for the first page
    end = start + 19  # Show 20 careers per page
    
    # Call the API to get careers
    response = get_careers(start=start, end=end, sort="name")

    # Extract careers list and pagination data
    careers_list = response.get("career", [])
    total = response.get("total", 0)  # Total number of careers
    
    # Calculate next and previous pagination indices
    next_start = start + 20 if end < total else None
    prev_start = start - 20 if start > 1 else None
    print(response)
    return render_template(
        "all_careers.html",
        careers=careers_list,
        current_start=start,
        prev_start=prev_start,
        next_start=next_start,
    )


@careers.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = []
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@careers.route("/careers/<career>", methods=["GET", "POST"])
def movie_detail(movie_id):
    try:
        result = []
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(imdb_id=movie_id)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews
    )
