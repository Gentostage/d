import pandas as pd
import json
from datetime import datetime

_HELLOSKILL = './db/hello_skill.csv'
_BYESKILL = './db/bye_skill.csv'
_FALLSKILL = './db/fallback_skill.csv'
# _skill = pd.read_csv(_FILESKILL)


def test():
    return 'test ok'


def save_skill(data):
    data = data['data']
    pd.DataFrame(data['data']).replace(r'^\s*$', 'NULL', regex=True).to_csv('./db/'+data['name']+'.csv', index=False,
                                                                            na_rep='NULL')
    return 'ok'


def get_skill():
    hello = pd.read_csv(_HELLOSKILL)
    bye = pd.read_csv(_BYESKILL)
    fall = pd.read_csv(_FALLSKILL)
    data = {
        'hello': hello.where((pd.notnull(hello)), None).to_dict(),
        'bye': bye.where((pd.notnull(bye)), None).to_dict(),
        'fallback': fall.where((pd.notnull(fall)), None).to_dict(),
    }
    return json.dumps(data, ensure_ascii=False)


def remove_skill(data):
    return 'ok'


def add_skill(data):
    return 'ok'


def init():
    bye = pd.DataFrame({'responses': ['Пока 1', 'Пока 2'], 'patterns': ['Пока 1', 'Пока 2']})
    bye.to_csv(_BYESKILL, index=False)