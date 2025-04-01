from model import Movie, Director, Genre, movie_genres
from config import db
from sqlalchemy import func

def get_all_movies():
    result = ( db.session.query(
        Movie.title.label('Фильм'),
        Director.name.label('Автор'),
        Genre.name.label('Жанр')
    )
               .join(Director, Movie.director_id == Director.id)
               .join(movie_genres, Movie.id == movie_genres.c.movie_id)
               .join(Genre, Genre.id == movie_genres.c.genre_id)
               .order_by(Genre.name)
             )
    return [result.statement.columns.keys(), result.all()]


# 1 Фильмы с рейтингом выше 8.5
def rating_top():
    result1 = (db.session.query(
        Movie.title.label("Название"),
        Movie.rating.label("Рейтинг")
    )
               .select_from(Movie)
               .filter(Movie.rating > 8.5)
               )
    return [result1.statement.columns.keys(), result1.all()]


# 2 Самые популярные жанры
def popular_genre():
    result2 = (db.session.query(
        Genre.name.label("Название"),
        func.count(Movie.id).label("Количество")
    )
               .join(movie_genres, Genre.id == movie_genres.c.genre_id)
               .join(Movie, Movie.id == movie_genres.c.movie_id)
               .group_by(Genre.name)
               .order_by(func.count(Movie.id).desc())
               )
    return [result2.statement.columns.keys(), result2.all()]


# 3 Средний рейтинг фильмов режиссера
def avg_rating():
    result3 = (db.session.query(
        Director.name,
        func.avg(Movie.rating)
    )
               .join(Movie)
               .group_by(Director.name)
               )
    return [result3.statement.columns.keys(), result3.all()]


# 4 Режиссеры которые сняли более 5 фильмов
def dir_more_5_films():
    result4 = (db.session.query(
        Director.name,
        func.count(Movie.id)
    )
               .join(Movie)
               .group_by(Director.name)
               .having(func.count(Movie.id) > 5)
               )
    return [result4.statement.columns.keys(), result4.all()]


# 5 Фильмы после 2000 года, отсортированные по рейтингу у которых жанр Comedy или Drama
def method_5():
    result5 = (db.session.query(
        Movie.title.label("Фильм"),
        Genre.name.label("Жанр"),
        Movie.year.label("Год"),
        Movie.rating.label("Рейтинг")
    )
               .join(movie_genres, Genre.id == movie_genres.c.genre_id)
               .join(Movie, Movie.id == movie_genres.c.movie_id)
               .filter(Movie.year > 2000, Genre.name == 'Comedy' or Genre.name == 'Drama')
               )
    return [result5.statement.columns.keys(), result5.all()]


# 6 вывести все фильмы относящиеся к самым популярным жанрам
def method_6():
    # Сначала создаем подзапрос для определения самых популярных 3 жанров
    subquery = (db.session.query(
        Genre.id,
        func.count(Movie.id).label("count")
    )
                .join(movie_genres, Genre.id == movie_genres.c.genre_id)
                .join(Movie, Movie.id == movie_genres.c.movie_id)
                .group_by(Genre.id)
                .order_by(func.count(Movie.id).desc())
                .limit(3)
                .subquery()
                )

    result6 = (db.session.query(
        Movie.title.label("Фильм"),
        Genre.name.label("Жанр"),
    )
               .join(movie_genres, Movie.id == movie_genres.c.movie_id)
               .join(Genre, Genre.id == movie_genres.c.genre_id)
               .filter(Genre.id.in_(db.session.query(subquery.c.id)))
               .group_by(Movie.title, Genre.name)
               .order_by(Genre.name)
               )
    return [result6.statement.columns.keys(), result6.all()]