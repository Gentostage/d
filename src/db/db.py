import pandas as pd
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

_HELLOSKILL = './db/hello_skill.csv'
_BYESKILL = './db/bye_skill.csv'
_FALLSKILL = './db/fallback_skill.csv'


# _skill = pd.read_csv(_FILESKILL)




def test():
    return 'test ok'


def save_skill(data):
    data = data['data']
    pd.DataFrame(data['data']).replace(r'^\s*$', 'NULL', regex=True).to_csv('./db/' + data['name'] + '.csv',
                                                                            index=False,
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


class User(UserMixin):
    username = ''
    USERS_FILE = './db/users.csv'
    password_hash = ''

    def __init__(self):
        import os.path
        if not os.path.exists(self.USERS_FILE):
            df = pd.DataFrame(columns=['login', 'password', 'token'])
            df.replace(r'^\s*$', 'NULL', regex=True).to_csv(self.USERS_FILE,
                                                            index=False,
                                                            na_rep='NULL')

    def get_hash(self, login: str) -> bool:
        df = pd.read_csv(self.USERS_FILE, encoding="utf-8")
        user = df.loc[df['login'] == login]
        if not user.empty:
            self.id = user.index.item()
            self.password_hash = user.at[0, 'password']
            return True
        else:
            return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def check_user(self, login: str) -> bool:
        df = pd.read_csv(self.USERS_FILE, encoding="utf-8")
        user = df.loc[df['login'] == login]
        if not user.empty:
            return True
        else:
            return False

    def create_new_user(self, login: str, password: str) -> str:
        if self.check_user(login):
            return 'Пользователь уже зарегистрирован'
        self.set_password(password)
        df = pd.read_csv(self.USERS_FILE, encoding="utf-8")
        print(login, self.password_hash)
        df = df.append({'login': login, 'password': self.password_hash}, ignore_index=True)
        df.replace(r'^\s*$', 'NULL', regex=True).to_csv(self.USERS_FILE,
                                                        index=False,
                                                        na_rep='NULL')
        return login

    def get_user(self,id: int):
        df = pd.read_csv(self.USERS_FILE, encoding="utf-8")
        user = df.loc[int(id)]
        self.username = user.at['login']
        return self