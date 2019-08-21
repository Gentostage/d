import csv, os, json, pandas
from app import app
from app import agent
from flask import Flask, request, render_template, redirect
from random import randint
from app.db import skill, qa


# API FAQ
@app.route("/api", methods=['GET', 'POST'])
def api():
    massage = ''
    if request.method == 'POST':
        data = request.data
        dataJson = json.loads(data)
        massage = dataJson['massage']
        if massage == '':
            return 'Error params, massage is null', 400

    if request.method == 'GET':
        massage = request.args.get('massage')
        if massage == '':
            return 'Error params, massage is null', 400

    a = str(agent.FAQ(massage))
    leng = len(a)
    a = a[2:leng - 2]
    return a


@app.route("/settings/relern")
def settings_relern():
    """ Обучаем """
    key = request.args.get('key')
    if key == 'ECA1B4346991DCB90A179D35AC49AC08':
        result = agent.relern()
        return result, 200


@app.route("/category", methods=['DELETE', 'PUT', 'POST'])
def category():
    """ Управление категориями """
    data = request.data
    dataDict = json.loads(data)

    if request.method == 'DELETE':  # Удалить
        name = dataDict['name']
        os.rename('./app/data/' + name + '.csv',
                  './app/data/deleted/' + str(randint(100000, 1000000)) + '_' + name + '.csv')
        return name, 200

    if request.method == 'PUT':  # Переименовать
        name = dataDict['name']
        newName = dataDict['newName']
        old = os.path.join('./app/data/', name + '.csv')
        new = os.path.join('./app/data/', newName + '.csv')
        os.rename(old, new)
        return new, 200

    if request.method == 'POST':  # Создание новой
        name = dataDict['name']
        #TODO Заменить на pandas
        with open('./app/data/' + name + '.csv', 'w+') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(["Question", "Answer"])
        return name, 200


@app.route("/setOld", methods=['GET', 'POST'])
def setOLD():
    """
    Сохранение всех вопросов и ответов на кнопку
    TODO Удалить
    """
    if request.method == 'POST':
        data = request.data
        tmpdata = json.loads(data)
        listdata = []
        for tmp in tmpdata['td']:
            templist = [tmp['qtext'], tmp['atext']]
            listdata.append(templist)
        with open('./app/data/' + tmpdata['name'], 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(["Question", "Answer"])  # Записать заголовок
            writer.writerows(listdata)
        return 'ok', 200
    else:
        return 'error', 400


@app.route("/data", methods=['GET', 'PUT', 'DELETE'])
def data():
    """ Категория """
    if request.method == 'GET':
        name = request.args.get('name')
        json_string = qa.open_file(name)
        return json_string

    if request.method == 'PUT': # Сохраняем
        data = request.data
        qa.save(data)
        return 'ok', 200

    if request.method == 'DELETE':
        data = request.data
        dataDict = json.loads(data)
        id = dataDict['id']
        name = './app/data/' + dataDict['name']
        df = pandas.read_csv(name)
        df = df.drop(id)
        df.to_csv(name, index=False)
        return 'ok', 200


@app.route("/data/list")
def data_list():
    """ Список категорий """
    files = (os.listdir(path="./app/data"))
    files.remove('dataset.csv')
    files.remove('deleted')
    return json.dumps(files)


@app.route("/skills", methods=['PUT', 'GET'])
def skills():
    """ Сохраниение и получение скиллов """
    if request.method == 'PUT':
        data = request.data
        skill.save_skill(json.loads(data))
        #agent.new_pattern_matching_skill()
        return 'ok', 200
    if request.method == 'GET':
        return skill.get_skill(), 200
