import sqlite3, math, time

from flask import flash

class DataBase:
    def __init__(self, db):
        self.__db = db 
        self.__cur = db.cursor()
    

    def addUser(self, name, email, password):
        try:
            self.__cur.execute(f'SELECT COUNT() AS `count` FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                flash('Такая почта занята', 'error')
                return False
            type_user = 'user'
            self.__cur.execute("INSERT INTO users (name, email, password, status) VALUES(?,?,?,?)", (name, email, password, type_user))
            self.__db.commit()
        except:
            print("Ошибка добавления пользователя")
            return False

        print("Регистрация прошла")
        return True

    def getUser(self, user_id):
            try:
                self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
                res = self.__cur.fetchone()
                if not res:
                    print("Пользователь не найден")
                    return False
                
                return res
                    
            except sqlite3.Error as e:
                print("Ошибка получения данных из БД" + str(e))
            
            return False
