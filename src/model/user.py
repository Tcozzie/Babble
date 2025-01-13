import datetime
from datetime import datetime as dt
from zoneinfo import ZoneInfo

from peewee import *

from src.model.base import BaseModel


class User(BaseModel):
    username = CharField()
    email = CharField()
    userID = CharField(primary_key=True)
    profilePic = CharField()
    joined_date = DateTimeField(default=lambda: datetime.datetime.now(ZoneInfo("America/Denver")))
    isFounder = BooleanField(default=False)
    subscription = BooleanField(default=False)

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

    def formatted_joined_date(cls):
        try:
            parsed_date = dt.strptime(cls.joined_date.split(".")[0],
                                      "%Y-%m-%d %H:%M:%S")
            return parsed_date.strftime("%b %d, %Y")
        except Exception:
            return cls.joined_date
