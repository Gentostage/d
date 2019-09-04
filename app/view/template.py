from flask import Flask, request, render_template, redirect, session
from flask_login import current_user, login_user, login_required, logout_user

from app import app
from app import login, user


@login.user_loader
def load_user(id):
    return user.get_user(id)


@app.route("/")
def index():
    return render_template('main.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route("/chat")
def chat():
    return render_template('chat.html')


# Страница с меню настроек
@app.route("/control/matching")
@login_required
def control_matching():
    return render_template('matching.html', navbar='on')


@app.route("/control/qa")
@login_required
def control_qa():
    return render_template('qa.html', navbar='on')


@app.route("/control/tree")
@login_required
def control_tree():
    return render_template('tree.html', navbar='on')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect('/')
        return render_template('login.html')

    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if not login or not password:
            return render_template('login.html', massage='Заполните все поля')
        if request.form.get('create'):
            result = user.create_new_user(login.lower(), password)
            if result == 'Пользователь уже зарегистрирован':
                return render_template('login.html', massage=result)
            return render_template('login.html', massage='Поздравляю ' + result + ' вы зарегистрированы')

        elif request.form.get('login'):
            result = user.get_hash(login.lower())
            if result:
                result = user.check_password(password)
                if result:
                    login_user(user, remember=login)
                    return redirect('/')
                else:
                    return render_template('login.html', massage='Неправильный логин или пароль пароль')
            else:
                return render_template('login.html', massage='Неправильный логин или пароль пароль')


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect('/')
