import pandas as pd
import os


def open_file(name):
    """ Считать фаил данных
    Name имя файла по дефолту первый
    """

    files = os.listdir(path="./app/data")
    # При загрузки страницы выдавал первый фаил не скомпилированный
    files.remove('dataset.csv')
    files.remove('deleted')
    if name == 'default':
        name = files[0]
    else:
        name = name + '.csv'
    # Считывания файла
    if name in files:
        ph = pd.read_csv('./app/data/' + name, encoding="utf-8")
        return ph.to_json(orient='records', force_ascii=False)


def save(data):
    """ Сохранение данных"""
    dataDict = json.loads(data)
    answer = dataDict['answer']
    question = dataDict['question']
    id = dataDict['id']
    name = './app/data/' + dataDict['name']
    df = pandas.read_csv(name)
    df.set_value(id, 'Question', question)
    df.set_value(id, 'Answer', answer)
    df.to_csv(name, index=False)
    return True
