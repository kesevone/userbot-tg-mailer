import configparser
import sqlite3

from core.variables import path_db

cfg = configparser.ConfigParser()


class DBConnect:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self):
        cfg.read('config.ini')
        self.connect = sqlite3.connect(cfg['DB']['PATH'], check_same_thread=False)
        self.cursor = self.connect.cursor()

    def create_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS data (timer INTEGER, interval INTEGER, photo_id TEXT, text TEXT)')
        self.connect.commit()

    def time_data(self, timer: int = None, interval: int = None, return_data: bool = False):
        data = self.cursor.execute('SELECT timer, interval FROM data').fetchone()
        if timer:
            if interval:
                if data is None:
                    self.cursor.execute('INSERT INTO data (timer, interval) VALUES (?, ?)', (timer, interval))
                else:
                    self.cursor.execute('UPDATE data SET timer=?, interval=?', (timer, interval))
            else:
                if data is None:
                    self.cursor.execute('INSERT INTO data (timer) VALUES (?)', (timer,))
                else:
                    self.cursor.execute('UPDATE data SET timer=?', (timer,))
        self.connect.commit()
        if return_data:
            return data

    def spam_data(self, photo_id: str = None, text: str = None, return_data: bool = False, delete: bool = False):
        data = self.cursor.execute('SELECT text, photo_id FROM data').fetchone()
        if text:
            if delete:
                self.cursor.execute('UPDATE data SET text=?', (None,))
            elif data is None:
                self.cursor.execute('INSERT INTO data (text) VALUES (?)', (text,))
            else:
                self.cursor.execute('UPDATE data SET text=?', (text,))
        if photo_id:
            if delete:
                self.cursor.execute('UPDATE data SET photo_id=?', (None,))
            elif data is None:
                self.cursor.execute('INSERT INTO data (photo_id) VALUES (?)', (photo_id,))
            else:
                self.cursor.execute('UPDATE data SET photo_id=?', (photo_id,))
        self.connect.commit()
        if return_data:
            return data