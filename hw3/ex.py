# 📌 Создать форму для регистрации пользователей на сайте.
# 📌 Форма должна содержать поля "Имя", "Фамилия", "Email", "Пароль" и кнопку "Зарегистрироваться".
# 📌 При отправке формы данные должны сохраняться в базе данных, а пароль должен быть зашифрован.

from flask import Flask, request, render_template
from flask_wtf.csrf import CSRFProtect

from ht_03_addOptionsOfFlask.forms_08 import RegistrationForm
from ht_03_addOptionsOfFlask.models_08 import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = '5adb2ded1ca80de778d7252a9036048fa6eaee4ebbcb2b204d2a682a46ba4b43'
csrf = CSRFProtect(app)
"""
Генерация надежного секретного ключа
>>> import secrets
>>> secrets.token_hex()
"""
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///ht03ex08.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        exist_user = User.query.filter(
            (User.firstname == firstname) or (User.lastname == lastname) or (User.email == email)
        ).first()
        if exist_user:
            error_msg = 'Username or email already exists.'
            form.firstname.errors.append(error_msg)
            return render_template('register.html', form=form)
        new_user = User(firstname=firstname, lastname=lastname,
                        email=email)
        new_user.set_pass(password)
        db.session.add(new_user)
        db.session.commit()
        success_msg = 'Registration successful!'
        return success_msg
    return render_template('register.html', form=form)


@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    users = User.query.all()
    return f'{list(users)}'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)