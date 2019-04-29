from flask import Flask, request, render_template

import deep as d

import csv
import json
import numpy as np
import time


app = Flask(__name__)

agent = d.deep()

@app.route("/")
def index():
    return render_template('main.html')

@app.route("/chat")
def chat():
    return render_template('chat.html')


# API FAQ
@app.route("/api", methods = ['GET','POST'])
def api():
    if request.method == 'POST':
        data = request.data 
        massage = json.loads(data)
        if massage == '':
            return 
        a = str(agent.FAQ(massage['massage']))
        leng = len(a)
        a = a[2:leng-2]
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
    with open('./data/'+agent.DATANAME, 'r') as fp:
        reader = csv.reader(fp, delimiter=',', quotechar='"')
        next(reader, None)  # Пропустить Заголовок
        data_read = [row for row in reader]

    json_string = json.dumps(data_read)

    return json_string
 
# Получние и управление 
@app.route("/settings")
def settings(): 
    data = request.args
    # Обучить
    if 'relenr' in data:
        if data['relenr'] == 'on':
            key = request.args.get('key')
            if key == 'ECA1B4346991DCB90A179D35AC49AC08':
                result=agent.relern()
                return result
    else:
        return "Bad param request "


# API Сохраннеие вопросов  
@app.route("/set" , methods = ['GET','POST'])
def set():
    if request.method == 'POST':
        data = request.data 
        tmpdata = json.loads(data) 
        listdata = []
        for tmp in tmpdata['td']:
            templist =[]
            templist.append(tmp['qtext'])
            templist.append(tmp['atext'])
            listdata.append(templist)
            
        with open('./data/'+agent.DATANAME, 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(["Question", "Answer"])  # Записать заголовок
            writer.writerows(listdata) 
        return 'ok'
    else:  
        return 'error'



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000 )


