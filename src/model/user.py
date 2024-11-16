from peewee import *
import logging

from src.model.base import BaseModel


class User(BaseModel):
    username = CharField()
    email = CharField()
    userID = CharField(primary_key=True)
    profilePic = CharField()

    @classmethod
    def all(cls, user_id, search=None):
        select = User.select()

        if search:
            select = select.where(User.username.ilike('%' + search + '%'))

        ## Remove the current user, no need to see themself
        filtered_out = []
        for user in select:
            if not (user_id == user.userID):
                filtered_out.append(user)

        return filtered_out

    @classmethod
    def find(cls, user_id):
        return User.get_or_none(User.userID == user_id)
