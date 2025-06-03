import sqlite3
import json

# Подключение к базе данных
conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

# Выполнение запроса
cursor.execute("SELECT * FROM movie")
movies = cursor.fetchall()

# Получение названий столбцов
column_names = [description[0] for description in cursor.description]

# Преобразование в список словарей
movies_list = []
for movie in movies:
    movie_dict = {}
    for i, column in enumerate(column_names):
        movie_dict[column] = movie[i]
    movies_list.append(movie_dict)

# Закрытие соединения
conn.close()

# Формирование JavaScript-файла
js_content = "const movies = " + json.dumps(movies_list, indent=4, ensure_ascii=False) + ";"

# Сохранение в файл
with open('movies.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Файл movies.js успешно создан")