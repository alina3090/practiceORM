from flask import jsonify, abort, request, Blueprint
from structures.models import (get_all_movies_with_links,
                               get_movie_by_id,
                               create_movie,
                               delete_movie_from_db,
                               get_movies_max_rating_by_year,
                               get_movies_min_rating_by_year,
                               get_avg_rating_by_year,
                               update_movie)

views = Blueprint("name", __name__)

@views.route('/structures/api/v1/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = get_movie_by_id(movie_id)
    if movie is None:
        abort(404, description="Movie not found")
    return jsonify(movie)

@views.route('/structures/api/v1/movies', methods=['POST'])
def add_movie():
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()

    required_fields = ['title', 'year']
    if not all(field in data for field in required_fields):
        abort(400, description=f"Missing required fields: {required_fields}")

    try:
        new_movie = create_movie(data)
        return jsonify(new_movie), 201
    except Exception as e:
        abort(500, description=str(e))


@views.route('/structures/api/v1/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    success = delete_movie_from_db(movie_id)
    if not success:
        abort(404, description="Movie not found")
    return jsonify({"message": f"Movie with ID {movie_id} deleted successfully"}), 200


@views.route('/structures/api/v1/movies', methods=['GET'])
def get_movies():
    search_param = request.args.get('search', '').upper()
    if search_param == 'MAXRATING':
        movies = get_movies_max_rating_by_year()
        return jsonify(movies)
    elif search_param == 'MINRATING':
        movies = get_movies_min_rating_by_year()
        return jsonify(movies)
    elif search_param == 'AVGRATING':
        avg_ratings = get_avg_rating_by_year()
        return jsonify({
            "_embedded": {"yearly_avg_ratings": avg_ratings},
            "_links": {
                "self": {"href": "/api/v1/movies?search=AVGRATING"}
            }
        })
    else:
        movies = get_all_movies_with_links()
        return jsonify({
            "_embedded": {"movies": movies},
            "_links": {"self": {"href": "/api/v1/movies"}}
        })


@views.route('/structures/api/v1/movies/<int:movie_id>', methods=['PATCH'])
def update_movie_route(movie_id):  # Измененное имя функции
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    try:
        updated = update_movie(movie_id, data)  # Вызов функции из models.py
        if not updated:
            abort(404, description="Movie not found")

        return jsonify({
            "id": updated.id,
            "title": updated.title,
            "year": updated.year,
            "rating": updated.rating,
            "director_id": updated.director_id,  # Добавлено
            "_links": {
                "self": {"href": f"/api/v1/movies/{updated.id}"},
                "director": {"href": f"/api/v1/directors/{updated.director_id}"},
                "genres": {"href": f"/api/v1/movies/{updated.id}/genres"}  # Добавлено
            }
        })
    except Exception as e:
        abort(400, description=str(e))