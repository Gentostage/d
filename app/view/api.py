from app import app
from app import agent
import csv
import json
import os
import pandas
from flask import Flask, request, render_template, redirect
from random import randint
from app.db import skill, qa

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
            old = os.path.join('./app/data/', data['name'] + '.csv')
            new = os.path.join('./app/data/', data['newName'] + '.csv')
            os.rename(old, new)
            return new, 200
        # Удалить категорию
        elif data['params'] == 'deleteCat':
            # os.remove('./app/data/'+data['name']+'.csv')
            os.rename('./app/data/' + data['name'] + '.csv',
                      './app/data/deleted/' + str(randint(100000, 1000000)) + '_' + data['name'] + '.csv')
            return data['name'], 200
        # Создать новый фаил с категорией
        elif data['params'] == 'newCat':
            with open('./app/data/' + data['name'] + '.csv', 'w+') as fp:
                writer = csv.writer(fp, delimiter=',')
                writer.writerow(["Question", "Answer"])
            return data['name'], 200
        else:
            return 'NO find params', 400
    else:
        return "Bad param request ", 400


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

    if request.method == 'PUT':
        data = request.data
        dataDict = json.loads(data)
        answer = dataDict['answer']
        question = dataDict['question']
        id = dataDict['id']
        name = './app/data/' + dataDict['name']
        df = pandas.read_csv(name)
        df.set_value(id, 'Question', question)
        df.set_value(id, 'Answer', answer)
        df.to_csv(name, index=False)
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
        agent.new_pattern_matching_skill()
        return 'ok', 200
    if request.method == 'GET':
        return skill.get_skill(), 200
