from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my.db' #указываем какая база данных
db = SQLAlchemy(app)
class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)  # Длинная ссылка (Text, так как URL бывают длинными)
    short_code = db.Column(db.String(10), unique=True, nullable=False)  # Короткий код, обязательно уникальный
@app.route("/", methods=['POST', 'GET'])
def zapros():
    if request.method == "POST":
        original_url = request.form.get('title')

        urlmap = URLMap(original_url=original_url, short_code=generate_short_code(6))
        try:
            db.session.add(urlmap)  # добавляем в базу данных
            db.session.commit()  # сохраняем
            return render_template("main.html", short_url=urlmap.short_code)
  # куда перенаправляем после заполнения всех полей
        except Exception as e:
            return f"произошла ошибка: {e}"
    else:
        return render_template("main.html")

def generate_short_code(length=6):
    # Берем все английские буквы (маленькие и большие) и цифры
    chars = string.ascii_letters + string.digits
    # Собираем случайную строчку нужной длины
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/<string:short_code>")

def poisk(short_code):
    db_record = URLMap.query.filter_by(short_code=short_code).first()
    if db_record:
        return redirect(db_record.original_url)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)

