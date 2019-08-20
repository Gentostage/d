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

