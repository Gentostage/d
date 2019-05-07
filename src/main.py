from flask import Flask, request, render_template

import deep as d
import db.db as db
import csv, json, os


app = Flask(__name__)

agent = d.deep()
# db = db.database()

#  Считать фаил данных
# Name имя файла по дефолту первый
def openfile(name):
    files = os.listdir(path="./data")
    # При загрузки страницы выдавал первый фаил не скомпилированный
    if name == 'default':
        if files[0]!='dataset.csv':
            name = files[0]
        else:
            name = files[1]
    else:
        name = name+'.csv'
    # Сам код считывания файла

    if name in files:
        print(name)
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


# API Получение списка вопросов
@app.route("/get")
def get():
    data = request.args
    if 'name' in data:
        json_string = openfile(data['name'])
        return json_string
    elif 'list' in data:
        files=(os.listdir(path="./data"))
        files.remove('dataset.csv')
        files = json.dumps(files)
        return files
    else:
        return 'Error name data'


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
                return result
    else:
        return "Bad param request "


# API Сохраннеие вопросов  
@app.route("/set", methods=['GET', 'POST'])
def set():
    if request.method == 'POST':
        data = request.data
        tmpdata = json.loads(data)
        listdata = []
        for tmp in tmpdata['td']:
            templist = [tmp['qtext'], tmp['atext']]
            listdata.append(templist)

        with open('./data/' + agent.DATANAME, 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(["Question", "Answer"])  # Записать заголовок
            writer.writerows(listdata)
        return 'ok'
    else:
        return 'error'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
