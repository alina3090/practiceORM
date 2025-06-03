from flask import Flask, jsonify
from config import db
app = Flask(__name__, static_folder="static")

# конфигурируем базу данных SQLite в папке instance приложения
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

# инициализируем приложение с расширением
db.init_app(app)

@app.route('/')
def hello_world():
 return jsonify({'app': 'top films'})

from structures.views import views

app.register_blueprint(views, url_prefix='/')

if __name__ == '__main__':
 print(app.url_map)
 app.run(host='0.0.0.0', port=5000)



