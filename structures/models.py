from model import Movie
from model import Movie, db
from sqlalchemy import func


def get_all_movies_with_links():
    movies = Movie.query.all()
    result = []
    for movie in movies:
        movie_data = {
            "id": movie.id,
            "title": movie.title,
            "year": movie.year,
            "rating": movie.rating,
            "_links": {
                "self": {
                    "href": f"/api/v1/movies/{movie.id}"
                },
                "director": {
                    "href": f"/api/v1/directors/{movie.director_id}"
                },
                "genres": {
                    "href": f"/api/v1/movies/{movie.id}/genres"
                }
            }
        }
        result.append(movie_data)
    return result


def get_movie_by_id(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        return {
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'rating': movie.rating,
            'director_id': movie.director_id
        }
    return None


def create_movie(movie_data):
    try:
        new_movie = Movie(
            title=movie_data['title'],
            year=movie_data['year'],
            rating=movie_data.get('rating'),  # .get() для необязательных полей
            director_id=movie_data.get('director_id')
        )
        db.session.add(new_movie)
        db.session.commit()
        return {
            'id': new_movie.id,
            'title': new_movie.title,
            'year': new_movie.year,
            'rating': new_movie.rating,
            'director_id': new_movie.director_id
        }
    except Exception as e:
        db.session.rollback()
        raise e


def delete_movie_from_db(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return False

    db.session.delete(movie)
    db.session.commit()
    return True


def get_movies_max_rating_by_year():
    # подзапрос для нахождения макс рейтинга по годам
    subquery = db.session.query(
        Movie.year,
        func.max(Movie.rating).label('max_rating')
    ).group_by(Movie.year).subquery()

    # Основной запрос для получения полной информации о фильмах
    results = db.session.query(Movie).join(
        subquery,
        (Movie.year == subquery.c.year) & (Movie.rating == subquery.c.max_rating)
    ).order_by(Movie.year.desc()).all()

    # Форматируем результат
    movies_by_year = {}
    for movie in results:
        if movie.year not in movies_by_year:
            movies_by_year[movie.year] = []
        movies_by_year[movie.year].append({
            'id': movie.id,
            'title': movie.title,
            'rating': float(movie.rating),
            'director_id': movie.director_id
        })

    return movies_by_year


def get_movies_min_rating_by_year():
    # Подзапрос для нахождения минимального рейтинга по годам
    subquery = (
        db.session.query(
            Movie.year,
            func.min(Movie.rating).label('min_rating')
        )
        .group_by(Movie.year)
        .subquery()
    )

    # Основной запрос с соединением
    results = (
        db.session.query(Movie)
        .join(
            subquery,
            (Movie.year == subquery.c.year) &
            (Movie.rating == subquery.c.min_rating)
        )
        .order_by(Movie.year.desc())
        .all()
    )

    # Форматируем результат с HATEOAS-ссылками
    movies_by_year = {}
    for movie in results:
        year = movie.year
        if year not in movies_by_year:
            movies_by_year[year] = []

        movies_by_year[year].append({
            "id": movie.id,
            "title": movie.title,
            "rating": float(movie.rating),
            "_links": {
                "self": {"href": f"/api/v1/movies/{movie.id}"},
                "director": {"href": f"/api/v1/directors/{movie.director_id}"},
                "genres": {"href": f"/api/v1/movies/{movie.id}/genres"}
            }
        })

    return movies_by_year

def get_avg_rating_by_year():
    results = db.session.query(
        Movie.year,
        func.round(func.avg(Movie.rating), 2).label('avg_rating'),
        func.count(Movie.id).label('movie_count')
    ).group_by(Movie.year).order_by(Movie.year.desc()).all()

    return [
        {
            "year": year,
            "avg_rating": float(avg_rating),
            "movie_count": count,
            "_links": {
                "movies": {"href": f"/api/v1/movies?year={year}"}
            }
        }
        for year, avg_rating, count in results
    ]


def update_movie(movie_id, update_data):
    movie = Movie.query.get(movie_id)
    if not movie:
        return None

    allowed_fields = {'title', 'year', 'rating', 'director_id'}
    updates = {k: v for k, v in update_data.items() if k in allowed_fields}

    try:
        for key, value in updates.items():
            setattr(movie, key, value)
        db.session.commit()
        return movie
    except Exception as e:
        db.session.rollback()
        raise e

