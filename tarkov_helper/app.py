from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.secret_key = '6a2b4f8c3e1d2a5b7c8e9f0a1b2c3d4e'

# Проверяем и создаем папки, если их нет
if not os.path.exists('../templates'):
    os.makedirs('../templates')
if not os.path.exists('../static/images'):
    os.makedirs('../static/images')

USERS_FILE = 'users.txt'


def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if ':' in line:
                    username, password_hash = line.strip().split(':', 1)
                    users[username] = password_hash
    return users


def save_user(username, password):
    with open(USERS_FILE, 'a') as f:
        f.write(f"{username}:{generate_password_hash(password)}\n")


@app.route('/')
def home():
    return render_template('main.html',
                           current_user={'is_authenticated': 'username' in session,
                                         'username': session.get('username')})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users:
            flash('Это имя пользователя уже занято', 'error')
        else:
            save_user(username, password)
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверное имя пользователя или пароль', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('home'))


# Страницы карт
@app.route('/epicentr')
def epicentr():
    return render_template('epicentr.html')


@app.route('/laboratoriya')
def laboratoriya():
    return render_template('laboratoriya.html')


@app.route('/les')
def les():
    return render_template('les.html')


@app.route('/mayak')
def mayak():
    return render_template('mayak.html')


@app.route('/razvyazka')
def razvyazka():
    return render_template('razvyazka.html')


@app.route('/rezerv')
def rezerv():
    return render_template('rezerv.html')


@app.route('/bereg')
def bereg():
    return render_template('bereg.html')


@app.route('/tamozhnya')
def tamozhnya():
    return render_template('tamozhnya.html')


@app.route('/zavod')
def zavod():
    return render_template('zavod.html')


@app.route('/ulicy')
def ulicy():
    return render_template('ulicy.html')


@app.route('/bullets')
def bullets():
    return render_template('bullets.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)