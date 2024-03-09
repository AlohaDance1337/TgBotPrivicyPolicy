import sqlite3
import datetime

class Database:
    def __init__(self)-> None:
        self.conn = sqlite3.connect('database.sqlite3')
        self.curs = self.conn.cursor()
        self.curs.execute('''
                    CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    chat_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    premium INTEGER DEFAULT 0,
                    admin INTEGER DEFAULT 0,
                    creator INTEGER DEFAULT 0
                    )
                    ''')
        self.conn.commit()

    def append_user(self, name: str = None, username: str = None, chat_id: int = None)-> None:
        if self.curs.execute("SELECT chat_id FROM Users WHERE chat_id = '{}'".format(chat_id)).fetchone()==None:
            self.curs.execute("INSERT INTO Users (name, username, chat_id, date) VALUES ('{}', '{}', '{}', '{}')".format(name, username!=None and '@'+username or username, chat_id, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")))
            self.conn.commit()

    def get_users_admin(self)-> list:
        return [item[0] for item in self.curs.execute("SELECT chat_id FROM Users WHERE admin=1").fetchall()]
    
    def get_users_premium(self)-> list:
        return [item[0] for item in self.curs.execute("SELECT premium FROM Users").fetchall()]
    
    def give_status_admin(self,chat_id:str=None):
            self.curs.execute('UPDATE Users SET admin=1 WHERE chat_id=?',(chat_id,))
            self.conn.commit()

    def give_status_premium(self,chat_id:str=None):
            self.curs.execute('UPDATE Users SET premium=1 WHERE chat_id=?',(chat_id,))
            self.conn.commit()

    def get_status(self, chat_id:int=None):
        return self.curs.execute("SELECT premium, admin,creator FROM Users WHERE chat_id=?", (chat_id,)).fetchall()

    def take_away_status(self, chat_id:int=None,status:str = None):
        if status == "take_away_premium":
            self.curs.execute('UPDATE Users SET premium=0 WHERE chat_id=?',(chat_id,))
            self.conn.commit()
        if status == "take_away_admin":
            self.curs.execute('UPDATE Users SET admin=0 WHERE chat_id=?',(chat_id,))
            self.conn.commit()
        if status == "take_away_creator":
            self.curs.execute('UPDATE Users SET creator=0 WHERE chat_id=?',(chat_id,))
            self.conn.commit()            
    
    def get_user(self, chat_id:int=None)->list[int]:
       return self.curs.execute("SELECT username FROM Users WHERE chat_id=?", (chat_id,)).fetchall()
       
    def get_users_username(self)-> list:
        return [item for item in self.curs.execute("SELECT username,date FROM Users").fetchall()]
    
    def get_users_chats_id(self)-> list:
        return [item[0] for item in self.curs.execute("SELECT chat_id FROM Users").fetchall()]
    
    def get_statistics(self,):
        return [item for item in self.curs.execute("SELECT * FROM Users").fetchall()]
    
    
    def get_last_10(self,):
        len_db = len(db.get_users_username())
        user_names = db.get_users_username()
        if len_db<=10:
            return user_names
        if len_db>10:
            a = len_db-10
            return user_names[a:len_db]

    def give_status_creator(self,chat_id:str=None):
        self.curs.execute('UPDATE Users SET creator=1 WHERE chat_id=?',(chat_id,))
