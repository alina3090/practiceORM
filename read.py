import csv

from config import db
from app import app
from model import Movie, Director, Genre, movie_genres

def parse_data(row): #Обработка сложных полей

    def parse_genres(val):
        return [g.strip() for g in val.split(',')] if val else []

    def parse_year(val):
        try:
            return int(''.join(filter(str.isdigit, val))) if val else None
        except:
            return 0

    return {
        'genres': parse_genres(row['Genre']),
        'year': parse_year(row['Released_Year'])
    }


with app.app_context():
    db.create_all()

    with open('all.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            #Director
            director_name = row['Director'].strip()
            director = Director.query.filter_by(name=director_name).first()

            if not director:
                director = Director(name=director_name)
                db.session.add(director)
                db.session.flush()


            # Парсинг данных
            data = parse_data(row)
            # Movie
            movie = Movie(
                title=row['Series_Title'],
                year=int(data['year']),
                rating=float(row['IMDB_Rating']),
                director_id=director.id
            )
            db.session.add(movie)
            db.session.flush()

            for genre_name in data['genres']:
                genre = Genre.query.filter_by(name=genre_name).first()

                if not genre:
                    genre = Genre(name=genre_name)
                    db.session.add(genre)
                    db.session.flush() # вместо коммита чтобы остаться в сессии

                if genre not in movie.genres:
                    movie.genres.append(genre)

            db.session.commit()

