from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd


class User(UserMixin):
    id = int
    username = ''
    USERS_FILE = './app/database/users.csv'
    password_hash = ''

    def __init__(self):
        import os.path
        if not os.path.exists(self.USERS_FILE):
            df = pd.DataFrame(columns=['login', 'password', 'token'])
            df.to_csv(self.USERS_FILE, index=False)

    def get_hash(self, login: str) -> bool:
        df = pd.read_csv(self.USERS_FILE, encoding="utf-8")
        user = df.loc[df['login'] == login]
        if not user.empty:
            self.id = user.index.item()
            self.password_hash = user.at[self.id, 'password']
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

    def get_user(self, id: int):
        df = pd.read_csv(self.USERS_FILE, encoding="utf-8")
        user = df.loc[int(id)]
        self.username = user['login']
        return self

    def get_id(self):
        return self.id