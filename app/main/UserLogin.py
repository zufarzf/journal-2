from flask_login import UserMixin
from app import db
from app.models import *

def getUser(user_id):
    user = Personal.query.filter_by(id=user_id).first()
    return user

class UserLogin(UserMixin):
    def fromDB(self, user_id):
        self.__user = getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)
