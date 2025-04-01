from config import db
from app import app

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))
    genres = db.relationship('Genre', secondary=movie_genres, backref='movies', cascade='all, delete')


class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    movies = db.relationship('Movie', backref='director', cascade='all, delete') # можно и back_populates зачем нам инит и почему не backref


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))


app.app_context().push()

with app.app_context():
    db.create_all()