from flask import Flask, request, render_template

import deep as d
import db.db as db
import csv, json, os
from random import randint

app = Flask(__name__)

agent = d.deep()
# db = db.database()

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
        name = name+'.csv'
    # Считывания файла
    if name in files:
        with open('./data/' + name, 'r') as fp:
            reader = csv.reader(fp, delimiter=',', quotechar='"')
            next(reader, None)  # Пропустить Заголовок
            data_read = [row for row in reader]
            json_string = json.dumps(data_read)
        return json_string


@app.route("/")
def index():
    return render_template('main.html')


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
@app.route("/answer")
def answer():
    return render_template('answer.html')


# Получение списка вопросов
@app.route("/get")
def get():
    data = request.args
    if 'name' in data:
        json_string = openfile(data['name'])
        return json_string
    elif 'list' in data:
        files=(os.listdir(path="./data"))
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
        if data['params'] == 'setNemaCategory':
            old = os.path.join('./data', data['name']+'.csv')
            new = os.path.join('./data', data['newName']+'.csv')
            os.rename(old, new)
            return new, 200
        elif data['params'] == 'deleteCat':
            #os.remove('./data/'+data['name']+'.csv')
            os.rename('./data/'+data['name']+'.csv','./data/deleted/'+str(randint(100000, 1000000))+'_'+data['name']+'.csv')
            return data['name'],200
        elif data['params'] == 'newCat':
            with open('./data/' + data['name']+'.csv', 'w+') as fp:
                writer = csv.writer(fp, delimiter=',')
                writer.writerow(["Question", "Answer"])
            return data['name'],200
    else:
        return "Bad param request ", 400


#Сохраннеие вопросов
@app.route("/set", methods=['GET', 'POST'])
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
