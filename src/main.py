import csv
import json
import os
import pandas
from random import randint
import deep as d
from db import db
from flask import Flask, request, render_template, redirect
from flask_login import current_user, login_user, login_required, logout_user
from flask_login import LoginManager


app = Flask(__name__)
agent = d.deep()
login = LoginManager(app)
login.login_view = 'login'
user = db.User()

@login.user_loader
def load_user(id):
    return user.get_user(id)

PROJECT_PATH = './'

try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(PROJECT_PATH, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            import random

            SECRET_KEY = ''.join(
                [random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = open(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters \
            to generate your secret key!' % SECRET_FILE)


# Считать фаил данных
# Name имя файла по дефолту первый
def openfile(name):
    files = os.listdir(path="./data")
    # При загрузки страницы выдавал первый фаил не скомпилированный
    files.remove('dataset.csv')
    files.remove('deleted')
    if name == 'default':
        name = files[0]
    else:
        name = name + '.csv'
    # Считывания файла
    if name in files:
        pd = pandas.read_csv('./data/' + name, encoding="utf-8")
        return pd.to_json(orient='records', force_ascii=False)


@app.route("/test")
def test():
    db.init()
    return SECRET_KEY, 200


@app.route("/")
def index():
    return render_template('main.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

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
            return 'Заполните все поля'
        if request.form.get('create'):
            result = user.create_new_user(login.lower(), password)
            if result == 'Пользователь уже зарегистрирован':
                return result
            return result
        elif request.form.get('login'):
            result = user.get_hash(login.lower())
            if result:
                result = user.check_password(password)
                if result:
                    login_user(user, remember = login)
                    next_page = request.args.get('next')
                    print(next_page)
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = '/'
                    return redirect(next_page)
                else:
                    return redirect('/login')
            else:
                return redirect('/login')


@app.route("/chat")
def chat():
    return render_template('chat.html')


# API FAQ
@app.route("/api", methods=['GET', 'POST'])
def api():
    if request.method == 'POST':
        data = request.data
        massage = json.loads(data)
        if massage == '':
            return
        a = str(agent.FAQ(massage['massage']))
        leng = len(a)
        a = a[2:leng - 2]
        return a
    else:
        return 'error wrong method'


# Страница с меню настроек
@app.route("/control/<type>")
@login_required
def control(type):
    if type == 'qa':
        return render_template('qa.html', navbar='on')
    elif type == 'matching':
        return render_template('matching.html', navbar='on')
    else:
        return redirect('/'), 401


# Получение списка вопросов
@app.route("/get")
def get():
    data = request.args
    if 'name' in data:
        json_string = openfile(data['name'])
        return json_string
    elif 'list' in data:
        files = (os.listdir(path="./data"))
        files.remove('dataset.csv')
        files.remove('deleted')
        files = json.dumps(files)
        return files
    else:
        return 'Error name data', 400


# Получние и управление 
@app.route("/settings")
def settings():
    data = request.args
    # Обучить
    if 'relenr' in data:
        if data['relenr'] == 'on':
            key = request.args.get('key')
            if key == 'ECA1B4346991DCB90A179D35AC49AC08':
                result = agent.relern()
                return result, 200
    elif 'params' in data:
        # Переименовать
        if data['params'] == 'renameCategory':
            old = os.path.join('./data', data['name'] + '.csv')
            new = os.path.join('./data', data['newName'] + '.csv')
            os.rename(old, new)
            return new, 200
        # Удалить категорию
        elif data['params'] == 'deleteCat':
            # os.remove('./data/'+data['name']+'.csv')
            os.rename('./data/' + data['name'] + '.csv',
                      './data/deleted/' + str(randint(100000, 1000000)) + '_' + data['name'] + '.csv')
            return data['name'], 200
        # Создать новый фаил с категорией
        elif data['params'] == 'newCat':
            with open('./data/' + data['name'] + '.csv', 'w+') as fp:
                writer = csv.writer(fp, delimiter=',')
                writer.writerow(["Question", "Answer"])
            return data['name'], 200
        else:
            return 'NO find params', 400
    else:
        return "Bad param request ", 400


# Сохраннеие вопросов
@app.route("/setOld", methods=['GET', 'POST'])
def set():
    if request.method == 'POST':
        data = request.data
        tmpdata = json.loads(data)
        listdata = []
        for tmp in tmpdata['td']:
            templist = [tmp['qtext'], tmp['atext']]
            listdata.append(templist)

        with open('./data/' + tmpdata['name'], 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(["Question", "Answer"])  # Записать заголовок
            writer.writerows(listdata)
        return 'ok', 200
    else:
        return 'error', 400


@app.route("/set", methods=['GET', 'POST', 'PUT', 'DELETE'])
def setTest():
    if request.method == 'PUT':
        data = request.data
        dataDict = json.loads(data)
        answer = dataDict['answer']
        question = dataDict['question']
        id = dataDict['id']
        name = './data/' + dataDict['name']
        df = pandas.read_csv(name)
        df.set_value(id, 'Question', question)
        df.set_value(id, 'Answer', answer)
        df.to_csv(name, index=False)
        return 'ok', 200
    elif request.method == 'DELETE':
        data = request.data
        dataDict = json.loads(data)
        id = dataDict['id']
        name = './data/' + dataDict['name']
        df = pandas.read_csv(name)
        df = df.drop(id)
        df.to_csv(name, index=False)
        return 'ok', 200
    else:
        return 'bad params', 401
    return 'error', 405


@app.route("/get/skills")
def get_skills():
    return db.get_skill(), 200


@app.route("/set/skills", methods=['PUT', 'GET'])
def set_skills():
    if request.method == 'PUT':
        data = request.data
        db.save_skill(json.loads(data))
        agent.new_pattern_matching_skill()
        return 'ok', 200
    else:
        return 'method not allow', 405


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return redirect('/')


if __name__ == "__main__":
    app.secret_key = SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'


    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=3000)
