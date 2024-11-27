import datetime

from peewee import *

from src.model.base import BaseModel


class User(BaseModel):
    username = CharField()
    email = CharField()
    userID = CharField(primary_key=True)
    profilePic = CharField()
    joined_date = DateTimeField(default=lambda: datetime.datetime.now().strftime('%b %d, %Y'))

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

    @classmethod
    def update_profile_pic(cls, user_id, new_profile_pic):
        query = User.update(profilePic=new_profile_pic).where(User.userID == user_id)
        rows_updated = query.execute()
        return rows_updated
