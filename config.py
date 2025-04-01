from flask_sqlalchemy import SQLAlchemy
from app import app

# создаем расширение
db = SQLAlchemy()

# конфигурируем базу данных SQLite в папке instance приложения
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

# инициализируем приложение с расширением
db.init_app(app)