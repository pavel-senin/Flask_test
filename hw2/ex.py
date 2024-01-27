# 📌 Создать страницу, на которой будет форма для ввода имени и электронной почты
# 📌 При отправке которой будет создан cookie файл с данными пользователя
# 📌 Также будет произведено перенаправление на страницу приветствия, где будет отображаться имя пользователя.
# 📌 На странице приветствия должна быть кнопка "Выйти"
# 📌 При нажатии на кнопку будет удален cookie файл с данными пользователя и произведено перенаправление
# на страницу ввода имени и электронной почты.

from flask import Flask, render_template, request, make_response, session, flash, url_for, redirect
from markupsafe import escape

app = Flask(__name__)
app.secret_key = b'f57f3a0bd0192d415028b4394165b34dbc95a97f1447aae754d9939180fe3db5'
# >>> import secrets
# >>> secrets.token_hex()


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/cookie/', methods=['POST'])
def cookie():
    username = request.form['name']
    usermail = request.form['mail']

    response = make_response(redirect('/hello/'))
    response.set_cookie('name', username)
    response.set_cookie('mail', usermail)
    return response


@app.route('/hello/')
def hello():
    username = request.cookies.get('name')
    usermail = request.cookies.get('mail')
    if not username or not usermail:
        flash('Введите имя и почту!', 'danger')
        return redirect(url_for('login'))
    flash('Форма успешно отправлена', 'success')
    return render_template('hello.html', name=username)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    context = {
        'task': 'Задание'
    }
    if request.method == 'POST':
        username = request.form.get('name')
        usermail = request.form.get('mail')
        context = {'username': username,
                   'usermail': usermail}
    return render_template('login.html', **context)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('name')
    response.delete_cookie('mail')
    return response


if __name__ == '__main__':
    app.run(debug=True)