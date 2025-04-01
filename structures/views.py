from app import app
from flask import render_template
from structures.models import get_all_movies, rating_top, popular_genre, avg_rating, dir_more_5_films,method_5, method_6


@app.route('/')
def index():

    [buildings_head, buildings_body] = get_all_movies()
    [rating_head, rating_body] = rating_top()
    [genre_head, genre_body] = popular_genre()
    [avg_rating_head, avg_rating_body] = avg_rating()
    [dir_head, dir_body] = dir_more_5_films()
    [method_5_head, method_5_body] = method_5()
    [method_6_head, method_6_body] = method_6()

    html = render_template(
        'index.html',
        buildings_head=buildings_head,
        buildings_body=buildings_body,
        rating_head=rating_head,
        rating_body=rating_body,
        genre_head=genre_head,
        genre_body=genre_body,
        avg_rating_head=avg_rating_head,
        avg_rating_body=avg_rating_body,
        dir_head=dir_head,
        dir_body=dir_body,
        method_5_head=method_5_head,
        method_5_body=method_5_body,
        method_6_head=method_6_head,
        method_6_body=method_6_body
    )

    return html