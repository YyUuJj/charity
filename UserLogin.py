from flask import url_for
from flask_login import UserMixin

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self
    
    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user['id'])
    
    def getName(self):
        return self.__user['name'] if self.__user else "Без имени"

    def getEmail(self):
        return self.__user['email'] if self.__user else "Без Email"
    
    # def verifyExt(self, filename):
    #     ext = filename.rsplit('.', 1)[1]
    #     if ext == "png" or ext == "PNG" or ext == "jpg" or ext == "JPG":
    #         return True
    #     return False